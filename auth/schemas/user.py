import uuid
from typing import List, Optional, Any

from pydantic import BaseModel, EmailStr, field_validator

from models.enums import UserRole


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    role: UserRole
    address: str
    city: str
    state: str
    zip_code: int = None
    phone: str = None
    lat: Optional[float] = None
    long: Optional[float] = None


    class Config:
        from_attributes = True


def is_string(value: Any) -> Any:
    if not isinstance(value, str):
        # convert the value to a string
        value = str(value)
        return value

class UserResponse(BaseModel):
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    role: str
    address: str
    city: str
    state: str
    zip_code: int = None
    phone: str = None
    hospital_created: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None

    @field_validator('user_id', mode='before')
    @classmethod
    def cast_instance(cls, value: Any) -> str | None:
        if not isinstance(value, str):
        # convert the value to a string
            return str(value)



    class Config:
        from_attributes = True
        arbitrary_types_allowed=True


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]


class LoginForm(BaseModel):
    username: str
    password: str
