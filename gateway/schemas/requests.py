from typing import Optional
from pydantic import BaseModel
from schemas import _enums


class RequestCreate(BaseModel):
    description: str
    request_type: _enums.RequestType
    request_status: _enums.RequestStatus
    hospital_id: Optional[str] = None
    requester_id: Optional[str] = None
    blood_type: _enums.BloodType
    quantity: int
    accepted_user_id: Optional[str] = None



