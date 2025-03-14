import os

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from dotenv import load_dotenv


from models.user import User
from models.enums import UserRole
from database import get_db

load_dotenv()

# security = HTTPBearer()



# Define a class to manage authentication
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE MINUTES")


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Generate JWT token
def create_access_token(data):
    payload = {
        "email": data.email,
        "user_id": data.user_id,
        "username": data.username,
        "role": data.role,
        "exp": datetime.utcnow() + timedelta(minutes=3600)  # Set expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Role-based access control dependencies
def is_donor(user: dict):
    if user["role"] != UserRole.DONOR.value:
        raise HTTPException(status_code=403, detail="Access denied: Donors only")
    return user

def is_admin(user: dict):
    if user["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Access denied: Donors admins only")
    return user

def is_requester(user: dict):
    if user["role"] != UserRole.REQUESTER.value:
        raise HTTPException(status_code=403, detail="Access denied: Requesters only")
    return user

def is_volunteer(user: dict):
    if user["role"] != UserRole.VOLUNTEER.value:
        raise HTTPException(status_code=403, detail="Access denied: Volunteers only")
    return user

def is_hospital_admin(user: dict):
    if user["role"] != UserRole.HOSPITAL_ADMIN.value:
        raise HTTPException(status_code=403, detail="Access denied: Hospital admins only")
    return user


def has_role(required_roles: list, user: dict):
    if user["role"] not in required_roles:
        raise HTTPException(status_code=403, detail=f"Access denied: Requires one of {required_roles}")
    return user



def validate_token(token: str):
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")


def replace_val(update_data: dict, user):
    """Replace None values in update_data with corresponding values from the user object."""
    for key, value in update_data.items():
        if value is None:  # If field is None, replace it with user's existing value
            update_data[key] = getattr(user, key, None)
    return update_data


