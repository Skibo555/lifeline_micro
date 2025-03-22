from enum import unique

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, create_engine, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


from . enums import UserRole
from database import Base
# from .request import Request
# from .donation import Donation


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(15), default=UserRole.DONOR.value, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(20), nullable=False)
    zip_code = Column(Integer)
    phone = Column(String(15))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    lat = Column(Float)
    long = Column(Float)


    hospital_created = Column(String(50), unique=True)

    # # Relationship: A user can create multiple hospitals
    # created_hospitals = relationship("Hospital", back_populates="created_by_user", cascade="all, delete-orphan")
    #
    # requests = relationship('Request', back_populates='requester')
    # donations = relationship('Donation', back_populates='donor')

    def __repr__(self):
        return f'<User {self.username} {self.email} {self.role}>'


# class Request(Base):
#     __tablename__ = 'requests'
#
#     request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
#     description = Column(String(250))
#     request_type = Column(String, nullable=False)
#     request_status = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
#
#     requester = relationship('User', back_populates='requests')
#
#     def __repr__(self):
#         return f'<Request {self.request_id} {self.request} {self.request_type} {self.request_status}>'
#
# class Donation(Base):
#     __tablename__ = 'donations'
#     donation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     donor_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
#     request_id = Column(UUID(as_uuid=True), ForeignKey('requests.request_id'), nullable=False)
#     donation_status = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     donor = relationship('User', back_populates='donations')
#
