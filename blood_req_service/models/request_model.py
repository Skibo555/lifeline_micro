from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, create_engine, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from database import Base

from .enums import RequestType, RequestStatus


class Request(Base):
    __tablename__ = 'requests'

    request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(250))
    request_type = Column(String(15), nullable=False, default=RequestType.NORMAL.value)
    request_status = Column(String(15), nullable=False, default=RequestStatus.PENDING.value)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    hospital_id = Column(UUID(as_uuid=True), nullable=False)
    requester_id = Column(String(50), nullable=False)
    blood_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    accepted_user_id = Column(ARRAY(String(50)), nullable=True)
    long = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)



    def __repr__(self):
        return f'<Request {self.request_id} {self.requester_id} {self.request_type} {self.request_status}>'

