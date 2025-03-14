# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, create_engine
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# import uuid
# from database import Base
# from models.user import User



# class Request(Base):
#     __tablename__ = 'requests'

#     request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
#     description = Column(String(250))
#     request_type = Column(String, nullable=False)
#     request_status = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#     requester = relationship('User', back_populates='requests')

#     def __repr__(self):
#         return f'<Request {self.request_id} {self.request} {self.request_type} {self.request_status}>'

