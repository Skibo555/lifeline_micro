import enum
import uuid

from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class HospitalStatus(enum.Enum):
    SUSPENDED = "suspended"
    ACTIVE = "active"


class HospitalType(enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"



class Hospital(Base):
    
    __tablename__ = "hospitals"
    hospital_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, unique=True, default=uuid.uuid4)
    name = Column(String(100), unique=True)
    address = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(20), nullable=False)
    type = Column(String(15), default=HospitalType.PRIVATE.value)
    status = Column(String(15), default=HospitalStatus.ACTIVE.value)
    zip_code = Column(Integer)
    phone = Column(String(15))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # This mimics how a reference to a foreignkey would work: Reference to the user who created the hospital
    created_by = Column(UUID(as_uuid=True), nullable=False)

    def __repr__(self):
        return f'<User {self.name} {self.email} {self.address}>'
