import time
import random
from fastapi import APIRouter, Body, Form, Depends, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/er")
async def emergency_treatment(patient_id: int = Form()):
    treatment_duration_hours = random.normalvariate(2, 0.5)
    treatment_duration_seconds = treatment_duration_hours * 1

    logger.info(
        f"Starting emergency treatment for patient_id: {patient_id}, "
        f"treatment duration (sim hours): {treatment_duration_hours:.2f}"
    )
    time.sleep(treatment_duration_seconds)
    phantom_pain = random.choice([True, False])
    logger.info(f"Completed emergency treatment for patient_id: {patient_id}, phantom pain: {phantom_pain}")

    return {"phantom_pain": phantom_pain, "needs_surgery": not phantom_pain}