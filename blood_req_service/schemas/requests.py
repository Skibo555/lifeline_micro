from pydantic import BaseModel
from typing import Optional


from models.enums import RequestStatus, RequestType


class RequestCreate(BaseModel):
    status: str
    description: str
    request_type: RequestType
    request_status: RequestStatus
    hospital_id: Optional[str] = None
    requester_id: Optional[str] = None
