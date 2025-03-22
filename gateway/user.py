from fastapi import APIRouter, status, Request, HTTPException, Depends
from auth_service import access

from schemas.users import UsernamePasswordForm, UserForm, UserUpdateForm, UserResponse, LoginResponse
from schemas.hospital import HospitalResponse, ListHospiatalResponse, CreateHospital, UpdateHospital


from utils import verify_token

server = APIRouter(tags=["User Gateway"], prefix="/gateway/users")


@server.post("/register", status_code=status.HTTP_200_OK)
def register(request: UserForm):
    response = access.register(request)
    
    return response


@server.post("/login", status_code=status.HTTP_200_OK)
def login(request: UsernamePasswordForm):
    response = access.login(request)

    return response
    

@server.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(request: UserUpdateForm,  user_id: str, token = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    response = access.update_user(request=request.model_dump(), user_id=user_id, token=token)

    return response


@server.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: str, user = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    response = access.get_user(user=user, user_id=user_id)

    return response


@server.get("", status_code=status.HTTP_200_OK)
def get_users(user = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    response = access.get_all_users(user=user)

    return response

    
@server.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id, user = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    response = access.delete_user(user=user, user_id=user_id)

    return response

