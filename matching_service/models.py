from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(15), nullable=False)
    address = Column(String, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(20), nullable=False)
    zip_code = Column(Integer)
    phone = Column(String(15))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    lat = Column(Float)
    long = Column(Float)

    def __repr__(self):
        return f'<User {self.username} {self.email} {self.role}>'


