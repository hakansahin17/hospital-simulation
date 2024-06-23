import time
import random
import logging
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from .database import get_db
from .models import Patient


router = APIRouter()
logger = logging.getLogger(__name__)


def determine_needs_surgery(diagnosis: str) -> bool:
    needs_surgery_diagnoses = {'A2', 'A3', 'A4', 'B3', 'B4'}
    return diagnosis in needs_surgery_diagnoses


@router.post("/intake")
async def intake_treatment(patient_id: int = Form(), db: Session = Depends(get_db)):
    treatment_duration_hours = random.normalvariate(1, 1/8)
    treatment_duration_seconds = treatment_duration_hours * 1

    logger.info(
        f"Starting normal treatment for patient_id: {patient_id}, "
        f"treatment duration (sim hours): {treatment_duration_hours:.2f}"
    )
    time.sleep(treatment_duration_seconds)
    logger.info(f"Completed intake treatment for patient_id: {patient_id}")

    diagnosis = db.query(Patient).get(patient_id).diagnosis

    needs_surgery = determine_needs_surgery(diagnosis)

    return {"phantom_pain": False, "needs_surgery": needs_surgery}