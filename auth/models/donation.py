# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# import uuid


# from database import Base
# from .user import User


# class Donation(Base):
#     __tablename__ = 'donations'
#     donation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     donor_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
#     request_id = Column(UUID(as_uuid=True), ForeignKey('requests.request_id'), nullable=False)
#     donation_status = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     donor = relationship('User', back_populates='donations')
