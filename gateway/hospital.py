from fastapi import APIRouter, status, Request, HTTPException, Depends
from auth_service import access

from schemas.hospital import HospitalResponse, ListHospiatalResponse, CreateHospital, UpdateHospital

from utils import verify_token
from auth_service import access

router = APIRouter(tags=["Hospital Gateway"], prefix="/gateway/hospitals")

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_hospital(request: CreateHospital, user = Depends(verify_token)):
    response = access.create_hospital(data=request.model_dump(), user=user)
    return response

@router.put("", status_code=status.HTTP_200_OK)
def update(data: UpdateHospital, hospital_id: str, user = Depends(verify_token)):
    response = access.update_hospital(hospital_id=hospital_id, user=user, data=data.model_dump())
    return response

@router.get("/{hospital_id}", status_code=status.HTTP_200_OK)
def get_hospital(hospital_id: str, user = Depends(verify_token)):
    response = access.get_hospital(user=user, hospital_id=hospital_id)
    return response

@router.get("", status_code=status.HTTP_200_OK)
def get_all_hospitals(user = Depends(verify_token)):
    response = access.get_all_hospital(user=user)
    return response

@router.delete("/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(hospital_id: str, user = Depends(verify_token)):
    access.delete_hospital(user=user, hospital_id=hospital_id)

    
