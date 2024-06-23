import time
import random
import logging
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from .database import get_db
from .models import Patient

router = APIRouter()
logger = logging.getLogger(__name__)


def determine_surgery_duration(diagnosis: str) -> float:
    duration_dict = {
        'A2': (1, 1 / 4),
        'A3': (2, 1 / 2),
        'A4': (4, 1 / 2),
        'B3': (16, 4),
        'B4': (16, 4),
        'EM': (2, 1 / 2)
    }
    mean, std_dev = duration_dict.get(diagnosis)
    return random.normalvariate(mean, std_dev)


@router.post("/surgery")
async def surgery(patient_id: int = Form(), db: Session = Depends(get_db)):
    diagnosis = db.query(Patient).get(patient_id).diagnosis
    treatment_duration_hours = determine_surgery_duration(diagnosis)
    treatment_duration_seconds = treatment_duration_hours * 1

    logger.info(
        f"Starting surgery for patient_id: {patient_id}, "
        f"surgery duration (sim hours): {treatment_duration_hours:.2f}"
    )
    time.sleep(treatment_duration_seconds)
    logger.info(f"Completed surgery treatment for patient_id: {patient_id}")
