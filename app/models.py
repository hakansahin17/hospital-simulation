from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_type = Column(String(2))
    diagnosis = Column(String(2))
    admission_date = Column(Integer)
    is_treated = Column(Boolean)


class Resource(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True, index=True)
    value = Column(Integer)
