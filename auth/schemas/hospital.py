from pydantic import BaseModel, EmailStr, field_validator
from models.enums import HospitalType, HospitalStatus
from typing import List, Any, Optional


class CreateHospital(BaseModel):
    name: str
    address: str
    email: EmailStr
    city: str
    state: str
    is_suspended: bool
    type: HospitalType
    status: HospitalStatus
    zip_code: int
    phone: str
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateHospital(BaseModel):
    name: str
    address: str
    phone: str


class HospitalResponse(BaseModel):
    hospital_id: str
    name: str
    address: str
    email: EmailStr
    city: str
    state: str
    is_suspended: bool
    type: HospitalType
    status: HospitalStatus
    zip_code: int
    phone: str
    created_by: str
    @field_validator('hospital_id', mode='before')
    @classmethod
    def cast_instance(cls, value: Any) -> str:
        if not isinstance(value, str):
        # convert the value to a string
            return str(value)
    @field_validator('created_by', mode='before')
    @classmethod
    def cast_inst(cls, value: Any) -> str:
        if not isinstance(value, str):
        # convert the value to a string
            return str(value)


class ListHospiatalResponse(BaseModel):
    hospitals: List[HospitalResponse]
