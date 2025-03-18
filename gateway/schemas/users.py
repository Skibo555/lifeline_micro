from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas import  _enums


class UsernamePasswordForm(BaseModel):
    username: str
    password: str


class UserForm(UsernamePasswordForm):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    role: _enums.UserRole
    address: str
    city: str
    state: str
    zip_code: int = None
    phone: str = None
    long: Optional[float] = None
    lat: Optional[float] = None


class UserUpdateForm(BaseModel):
    # username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    # middle_name: str = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[int] = None
    phone: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    user_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    role: str
    address: str
    city: str
    state: str
    zip_code: int
    phone: str
    created_at: str
    updated_at: str
