import os

from fastapi import HTTPException, status

from dotenv import load_dotenv


from models.hospital_model import Hospital, HospitalStatus, HospitalType, UserRole


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


