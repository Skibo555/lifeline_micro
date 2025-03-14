from fastapi import APIRouter, Depends, status, HTTPException, Request
from schemas.hospital import CreateHospital, UpdateHospital, HospitalResponse, ListHospiatalResponse
from sqlalchemy.orm import Session
from models.hospital import Hospital
from sqlalchemy import update as sqlalchemy_update
from models.enums import UserRole

from utils import (
    get_db,
    has_role
    )


router = APIRouter(prefix="/hospitals", tags=["Hospital Management"])


@router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=HospitalResponse)
async def create(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    current_user = data["user_data"]
    hospital_data = data["hospital_data"]
    has_role(
        required_roles=[UserRole.ADMIN.value, UserRole.HOSPITAL_ADMIN.value], user=current_user)
    hospital_data["created_by"] = current_user["user_id"]
    existing_hospitals = db.query(Hospital).filter(Hospital.created_by == current_user["user_id"]).first()
    if existing_hospitals:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not have more than one hospital.")
    if not existing_hospitals:
        hospital_data["created_by"] = current_user["user_id"]
        hospitals = db.query(Hospital).filter(Hospital.name == hospital_data["name"]).first()
        if hospitals:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There is an hospital with the email or name you used. Chose another email or name.")
        try:
            new_hospital = Hospital(hospital_data)
            db.add(new_hospital)
            db.commit()
            db.refresh(new_hospital)
            return new_hospital
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@router.put('', status_code=status.HTTP_200_OK, response_model=HospitalResponse)
async def update(data: UpdateHospital, current_user: dict, hospital_id: str, db: Session = Depends(get_db)):
    has_role(
        required_roles=[UserRole.ADMIN.value, UserRole.HOSPITAL_ADMIN.value], user=current_user)
    existing_hospital = db.query(Hospital).filter(Hospital.created_by == current_user["user_id"], Hospital.hospital_id == hospital_id).first()
    if not existing_hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="The hospital might not be created by this user.")
    stmt = sqlalchemy_update(Hospital).where(Hospital.hospital_id == hospital_id).values(**data.model_dump())
    db.execute(stmt)
    db.commit()
    db.refresh(existing_hospital)
    return existing_hospital


@router.get("/{hospital_id}", status_code=status.HTTP_200_OK)
async def get_hospital(hospital_id: str, user: dict, db: Session = Depends(get_db)):
    has_role(
        required_roles=[UserRole.DONOR.value, UserRole.ADMIN.value,
                        UserRole.HOSPITAL_ADMIN.value, UserRole.REQUESTER.value,
                        UserRole.VOLUNTEER.value], user=user)
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
        required_roles=[UserRole.DONOR.value, UserRole.ADMIN.value,
                        UserRole.HOSPITAL_ADMIN.value, UserRole.REQUESTER.value,
                        UserRole.VOLUNTEER.value], user=user)
    try:
        hospitals = db.query(Hospital).all()
        return hospitals
    except Exception as ex:
        print(ex)


@router.delete("/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(hospital_id: str, current_user: dict, db: Session = Depends(get_db)):
    has_role(required_roles=[UserRole.ADMIN.value, UserRole.HOSPITAL_ADMIN.value], user=current_user)
    owner_id = current_user["user_id"]
    existing_hospitals = db.query(Hospital).filter(Hospital.created_by == owner_id, Hospital.hospital_id == hospital_id).first()
    if not existing_hospitals:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user might not the the creator of the hospital.")
    db.delete(existing_hospitals)
    db.commit()
