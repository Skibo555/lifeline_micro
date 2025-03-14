from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update

from database import get_db
from models.request_model import Request as RequestModel, RequestStatus
from models.enums import UserRole
from rabbitmq_utils import publish_event
from utils import has_role


# from schemas.requests import RequestCreate


router = APIRouter(tags=["Blood request service"], prefix="/requests")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_request(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_info = data.get('user_data')
    request_data = data.get('request')
    hospital_id = data.get('hospital_id')

    new_request = RequestModel(
        description=request_data.get('description'),
        request_type=request_data.get('request_type'),
        request_status=request_data.get('request_status'),
        hospital_id=hospital_id,
        requester_id=user_info.get('user_id'),
        blood_type=request_data.get('blood_type'),
        quantity=request_data.get('quantity'),
        accepted_user_id=[]
    )

    try:
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        publish_event('request.created', new_request)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{request_id}", status_code=status.HTTP_200_OK)
async def get_request_with_id(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    request_id = req.get('request_id')
    current_user = req.get('user')
    has_role(required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=current_user)
    
    request = db.query(RequestModel).filter(RequestModel.request_id == request_id).first()

    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request


@router.get("/{status}", status_code=status.HTTP_200_OK)
async def get_requests_with_status(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    request_status = request.get('status')
    current_user = req.get('user')
    has_role(required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=current_user)
    
    requests = db.query(RequestModel).filter(RequestModel.request_status == request_status).all()

    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No requests found")
    return requests

@router.get("", status_code=status.HTTP_200_OK)
async def get_requests(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    current_user = req.get('user')
    has_role(required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=current_user)
    
    requests = db.query(RequestModel).all()
    print(request)
    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No requests found")
    return requests


@router.patch("{request_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_request(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    request_id = req.get('request_id')
    current_user = req.get('user')
    has_role(required_roles=[UserRole.ADMIN, UserRole.HOSPITAL_ADMIN], user=current_user)

    request = db.query(RequestModel).filter(RequestModel.requester_id == request_id, RequestModel.requester_id == current_user["user_id"]).first()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found or you are not your request owner")
    # if request.requester_id != current_user['user_id']:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this request, only the owner can cancel it.")
    stmt = sqlalchemy_update(RequestModel).where(RequestModel.request_id == request_id).values(request_status=RequestStatus.CANCELLED)
    db.execute(stmt)
    db.commit()
    publish_event('request.cancelled', request)


@router.patch("{request_id}/accept", status_code=status.HTTP_200_OK)
async def accept_request(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    request_id = req.get('request_id')
    current_user = req.get('user')
    has_role(required_roles=[UserRole.DONOR, UserRole.ADMIN,
                        UserRole.HOSPITAL_ADMIN, UserRole.REQUESTER,
                        UserRole.VOLUNTEER], user=current_user)
    request = db.query(RequestModel).filter(RequestModel.requester_id == request_id).first()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found.")
    # if request.requester_id != current_user['user_id']:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this request, only the owner can cancel it.")

    stmt = sqlalchemy_update(RequestModel).where(RequestModel.request_id == request_id).values(request_status=RequestStatus.CANCELLED)
    db.execute(stmt)
    db.commit()
    publish_event('request.accepted', request)
