from fastapi import APIRouter, Depends, status, HTTPException, Request
from schemas.hospital import CreateHospital, UpdateHospital, HospitalResponse, ListHospitalResponse
from sqlalchemy.orm import Session
from models.hospital_model import Hospital, UserRole
from sqlalchemy import update as sqlalchemy_update

from database import get_db
from rabbitmq_utils import publish_event

from utils import (
    has_role
    )


router = APIRouter(prefix="/hospitals", tags=["Hospital Management"])


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        current_user = data["user_data"]
        hospital_data = data["hospital_data"]
        has_role(
            required_roles=[UserRole.ADMIN, UserRole.HOSPITAL_ADMIN], user=current_user)
        existing_hospitals = db.query(Hospital).filter(Hospital.created_by == current_user["user_id"]).first()
        if existing_hospitals:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not have more than one hospital.")
        if not existing_hospitals:
            hospital_data["created_by"] = current_user["user_id"]
            hospitals = db.query(Hospital).filter(Hospital.name == hospital_data["name"]).first()
            if hospitals:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There is an hospital with the email or name you used. Chose another email or name.")
            # try:
            new_hospital = Hospital(**hospital_data)
            db.add(new_hospital)
            db.commit()
            db.refresh(new_hospital)

            # Publish event to RabbitMQ
            #await publish_event("hospital.created", **new_hospital.__dict__)
            return new_hospital

    except Exception as ex:
        print(ex)
        return ex

@router.put('', status_code=status.HTTP_200_OK)
async def update(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    current_user = data["user_data"]
    hospital_id = data["hospital_id"]
    update_data = data["hospital_data"]
    has_role(
        required_roles=[UserRole.ADMIN, UserRole.HOSPITAL_ADMIN], user=current_user)
    existing_hospital = db.query(Hospital).filter(Hospital.created_by == current_user["user_id"], Hospital.hospital_id == hospital_id).first()
    if not existing_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="The hospital might not be created by this user.")
    stmt = sqlalchemy_update(Hospital).where(Hospital.hospital_id == hospital_id).values(**update_data)
    db.execute(stmt)
    db.commit()
    db.refresh(existing_hospital)

    # Publish event to RabbitMQ
    await publish_event("hospital.updated", **existing_hospital.__dict__)
    return existing_hospital


@router.get("/{hospital_id}", status_code=status.HTTP_200_OK)
async def get_hospital(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    current_user = data["user_data"]
    hospital_id = data["hospital_id"]
    has_role(
        required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=current_user)
    try:
        existing_hospitals = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
        print(existing_hospitals)
        if not existing_hospitals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return existing_hospitals
    except Exception as ex:
        return "Invalid hospital id."


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_hospital(user: dict, db: Session = Depends(get_db)):
    has_role(
        required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=user)
    try:
        hospitals = db.query(Hospital).all()
        return hospitals
    except Exception as ex:
        print(ex)


@router.delete("/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    current_user = data["user_data"]
    hospital_id = data["hospital_id"]
    has_role(required_roles=[UserRole.ADMIN, UserRole.HOSPITAL_ADMIN], user=current_user)
    owner_id = current_user["user_id"]
    existing_hospitals = db.query(Hospital).filter(Hospital.created_by == owner_id, Hospital.hospital_id == hospital_id).first()
    if not existing_hospitals:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user might not the the creator of the hospital.")
    db.delete(existing_hospitals)

    # Publish event to RabbitMQ
    await publish_event("hospital.deleted", existing_hospitals.__dict__)
    db.commit()
