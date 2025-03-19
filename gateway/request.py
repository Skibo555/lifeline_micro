from fastapi import APIRouter, status, HTTPException, Request, Depends


from schemas.requests import RequestCreate
from schemas._enums import RequestStatus
from utils import verify_token
from auth_service import access

router = APIRouter(tags=["Request Gateway"], prefix="/gateway/requests")


# Create a request
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_request(request: RequestCreate, user = Depends(verify_token)):
    response = access.make_request(req=request.model_dump(), user=user)
    return response


# get a request with an id
@router.get("/{request_id}", status_code=status.HTTP_200_OK)
async def get_request(request_id: str, user = Depends(verify_token)):
    response = access.get_request_single(request_id=request_id, user=user)
    return response


# get all requests based on their status
@router.get("", status_code=status.HTTP_200_OK)
async def get_requests(request_status: RequestStatus, user = Depends(verify_token)):
    print(f"The status: {request_status.value}")
    response = access.get_requests(user=user, req_status=request_status.value)
    return response


# cancel a request
@router.patch("/{request_id}/cancel", status_code=status.HTTP_200_OK)
async def cancle_request(request_id: str, user = Depends(verify_token)):
    response = access.cancel_request(user=user, request_id=request_id)
    return response


# accept a request
@router.patch("/{request_id}/accept", status_code=status.HTTP_200_OK)
async def accept(request_id: str, user = Depends(verify_token)):
    response = access.accept_request(user=user, request_id=request_id)
    return response

