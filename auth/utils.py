import os

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends, status
from sqlalchemy.sql import func


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


# utility to find a match for a request
async def match(request: dict, radius_km: float = 10, db: Session = Depends(get_db)):
    """Find users within a radius using the Haversine formula"""
    data = request
    hospital_lat = data["lat"]
    hospital_long = data["long"]
    distance_expr = 6371 * func.acos(
        func.cos(func.radians(hospital_lat)) * func.cos(func.radians(User.lat)) *
        func.cos(func.radians(User.long) - func.radians(hospital_long)) +
        func.sin(func.radians(hospital_lat)) * func.sin(func.radians(User.lat))
    )

    return db.query(User, distance_expr.label("distance")) \
        .filter(User.lat.isnot(None), User.long.isnot(None)) \
        .having(distance_expr <= radius_km) \
        .order_by(distance_expr) \
        .all()

    # Example usage
    # db = SessionLocal()
    # user_lat = 4.8156  # Replace with actual user latitude
    # user_long = 7.0498  # Replace with actual user longitude
    #
    # nearby_users = find_nearby_users(db, user_lat, user_long)
    # db.close()
    #
    # # Print result
    # for user, distance in nearby_users:
    #     print(f"{user.username} is {distance:.2f} km away")


def match_users(request_data: dict, db: Session):
    """Find users within 10km using the Haversine formula"""
    hospital_lat = request_data["lat"]
    hospital_long = request_data["long"]

    distance_expr = 6371 * func.acos(
        func.cos(func.radians(hospital_lat)) * func.cos(func.radians(User.lat)) *
        func.cos(func.radians(User.long) - func.radians(hospital_long)) +
        func.sin(func.radians(hospital_lat)) * func.sin(func.radians(User.lat))
    )

    matches = db.query(User, distance_expr.label("distance")) \
        .filter(User.lat.isnot(None), User.long.isnot(None)) \
        .having(distance_expr <= 10) \
        .order_by(distance_expr) \
        .all()

    return matches


