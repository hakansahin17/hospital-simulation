import time
import random
import logging
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from .database import get_db
from .models import Patient

router = APIRouter()
logger = logging.getLogger(__name__)


def determine_nursing_duration(diagnosis: str) -> float:
    duration_dict = {
        'A1': (4, 1 / 2),
        'A2': (8, 2),
        'A3': (16, 2),
        'A4': (16, 2),
        'B1': (8, 2),
        'B2': (16, 2),
        'B3': (16, 4),
        'B4': (16, 4),
        'EM': (2, 1 / 2)
    }
    mean, std_dev = duration_dict.get(diagnosis)
    return random.normalvariate(mean, std_dev)


def determine_complication(diagnosis: str) -> bool:
    complication_chances = {
        'A1': 0.01,
        'A2': 0.01,
        'A3': 0.02,
        'A4': 0.02,
        'B1': 0.001,
        'B2': 0.01,
        'B3': 0.02,
        'B4': 0.02,
        'EM': 0.0
    }
    chance = complication_chances.get(diagnosis, 0.0)
    return random.random() < chance


@router.post("/nurse")
async def nurse(patient_id: int = Form(), db: Session = Depends(get_db)):
    diagnosis = db.query(Patient).get(patient_id).diagnosis
    treatment_duration_hours = determine_nursing_duration(diagnosis)
    treatment_duration_seconds = treatment_duration_hours * 1

    logger.info(
        f"Starting nursing for patient_id: {patient_id}, "
        f"Nursing duration (sim hours): {treatment_duration_hours:.2f}"
    )
    time.sleep(treatment_duration_seconds)
    was_complication = determine_complication(diagnosis)
    logger.info(f"Completed nursing treatment for patient_id: {patient_id}, was_complication: ")

    return {"was_complication": was_complication}
