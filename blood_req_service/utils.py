from fastapi import HTTPException, status

from enum import Enum

from sqlalchemy.sql import func
from sqlalchemy.orm import Session


class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    REQUESTER = "requester"
    HOSPITAL_ADMIN = "hospital_admin"
    VOLUNTEER = "volunteer"

# Role-based access control dependencies

def is_donor(user: dict):
    if user["role"] != UserRole.DONOR.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Donors only")
    return user

def is_admin(user: dict):
    if user["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Donors admins only")
    return user

def is_requester(user: dict):
    if user["role"] != UserRole.REQUESTER.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Requesters only")
    return user

def is_volunteer(user: dict):
    if user["role"] != UserRole.VOLUNTEER.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Volunteers only")
    return user

def is_hospital_admin(user: dict):
    if user["role"] != UserRole.HOSPITAL_ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Hospital admins only")
    return user


def has_role(required_roles: list, user: dict):
    if user["role"] not in required_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied: Requires one of {required_roles}")
    return user


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

