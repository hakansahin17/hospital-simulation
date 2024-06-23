from pydantic import BaseModel


class AdmissionBase(BaseModel):
    patient_type: str
    admission_date: int


class AdmissionCreate(AdmissionBase):
    pass


class Admission(AdmissionBase):
    id: int

    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    resource_id: str
    value: int


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    class Config:
        from_attributes = True
