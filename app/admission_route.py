import random
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import AdmissionCreate
from .models import Patient, Resource
from .database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


def determine_diagnosis(patient_type):
    probabilities = {
        'A': (['A1', 'A2', 'A3', 'A4'], [1 / 2, 1 / 4, 1 / 8, 1 / 8]),
        'B': (['B1', 'B2', 'B3', 'B4'], [1 / 2, 1 / 4, 1 / 8, 1 / 8]),
        'EM': (['EM'], [1])
    }
    choices, weights = probabilities[patient_type]
    return random.choices(choices, weights=weights, k=1)[0]


def check_resource_availability(diagnosis: str, arrival_time: int, db: Session) -> bool:
    arrival_datetime = datetime.fromtimestamp(arrival_time)
    requirements = {
        'A1': {'intake': 1, 'nursing_a': 1},
        'A2': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'A3': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'A4': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'B1': {'intake': 1, 'nursing_b': 1},
        'B2': {'intake': 1, 'nursing_b': 1},
        'B3': {'intake': 1, 'surgery': 1, 'nursing_b': 1},
        'B4': {'intake': 1, 'surgery': 1, 'nursing_b': 1},
        'EM': {'er': 1, 'surgery': 1, 'nursing_a_or_b': 1}
    }
    required_resources = requirements.get(diagnosis)

    if not required_resources:
        return False

    day_of_week = arrival_datetime.weekday()
    hour_of_day = arrival_datetime.hour

    available_intakes = db.query(Resource).filter_by(id='intake').first()
    if 'intake' in required_resources:
        if day_of_week >= 5 or hour_of_day < 8 or hour_of_day >= 17:
            return False
        elif available_intakes.value < required_resources['intake']:
            return False

    available_surgeries = db.query(Resource).filter_by(id='surgery').first()
    if 'surgery' in required_resources:
        if day_of_week < 5 and 8 <= hour_of_day < 17 and available_surgeries.value < required_resources['surgery']:
            return False
        elif available_surgeries.value < 5:
            return False

    for resource, amount in required_resources.items():
        if resource == 'nursing_a_or_b':
            nursing_a = db.query(Resource).filter_by(id='nursing_a').first()
            nursing_b = db.query(Resource).filter_by(id='nursing_b').first()
            if max(nursing_a.value, nursing_b.value) < amount:
                return False
        elif resource == 'nursing_a' or resource == 'nursing_b':
            available = db.query(Resource).filter_by(id=resource).first()
            if available.value < amount:
                return False

    # Decrement resources if available
    if 'intake' in required_resources:
        available_intakes.value -= required_resources['intake']

    if 'surgery' in required_resources:
        available_surgeries.value -= required_resources['surgery']

    for resource, amount in required_resources.items():
        if resource == 'nursing_a_or_b':
            nursing_a = db.query(Resource).filter_by(id='nursing_a').first()
            nursing_b = db.query(Resource).filter_by(id='nursing_b').first()
            if nursing_a.value >= amount:
                nursing_a.value -= amount
            else:
                nursing_b.value -= amount
        elif resource == 'nursing_a' or resource == 'nursing_b':
            available = db.query(Resource).filter_by(id=resource).first()
            available.value -= amount

    db.commit()
    return True


@router.post("/admission")
def create_admission(admission: AdmissionCreate, db: Session = Depends(get_db)):
    logger.info(f"Received admission request for patient at: {admission.admission_date}")
    diagnosis = determine_diagnosis(admission.patient_type)

    db_admission = Patient(
        patient_type=admission.patient_type,
        diagnosis=diagnosis,
        admission_date=admission.admission_date,
        is_treated=False,
    )
    db.add(db_admission)
    db.commit()
    db.refresh(db_admission)

    resources_available = check_resource_availability(diagnosis, admission.admission_date, db)

    logger.info(
        f"Created admission record for patient: {db_admission.id} with diagnosis: {db_admission.diagnosis},"
        f" resources available: {resources_available}"
    )

    return {"id": db_admission.id, "resources_available": resources_available}
