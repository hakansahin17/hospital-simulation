import logging
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from config import Config
from .database import get_db
from .models import Patient, Resource


router = APIRouter()
logger = logging.getLogger(__name__)


def release_resources(diagnosis: str, nursing_dep: str, db: Session):
    requirements = Config.RESOURCE_REQUIREMENTS.get(diagnosis, {})

    for resource, amount in requirements.items():
        if "nursing" not in resource:
            resource_obj = db.query(Resource).filter_by(id=resource).first()
            resource_obj.value += amount

    nursing_resource = db.query(Resource).get(f"nursing_{nursing_dep.lower()}")
    nursing_resource.value += 1


@router.post("/release")
async def release(patient_id: int = Form(), db: Session = Depends(get_db)):
    patient = db.query(Patient).get(patient_id)
    release_resources(patient.diagnosis, patient.nursing_department, db)
    patient.is_treated = True
    db.commit()
    logger.info(f"Released resources for patient_id: {patient_id}")
