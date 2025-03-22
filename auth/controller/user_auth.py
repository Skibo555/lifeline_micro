import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from fastapi import APIRouter, status, Depends, Response, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import exc

from database import get_db
from rabbitmq_service.communications.rabbitmq_publisher import rabbitmq_service

from schemas.user import UserCreate, UserResponse, UserListResponse, LoginForm
from models.user import User
from utils import (
    hash_password,
    verify_password,
    create_access_token,
    replace_val,
    has_role
    )
from models.enums import UserRole


app = APIRouter(tags=["Authentication Service"], prefix="/auth/users")


# Register a new user
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        # elif existing_user.username == user.username:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Someone else uses that username")

        # Hash password & save user
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()

        db.refresh(new_user)

        message = "User account created successfully!"
        user_data = {
            "username": user.username,
            "user_id": str(new_user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": str(new_user.created_at),
            "updated_at": str(new_user.updated_at),
            "address": new_user.address,
            "is_active": user.is_active,
            "email": user.email,
            "role": user.role,
            "state": user.state,
            "city": user.city,
            "long": user.long,
            "lat": user.lat
        }

        await rabbitmq_service.publish_event(event_name="user.created", data=user_data)

        return {
            "message": message,
            "data": user_data
        }

    except exc.IntegrityError as ex:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Someone else uses that username")

    # except Exception as ex:
    #     print(f"I got GLOBAL EXCEPTION {ex}")
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something unexpected happened")


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: LoginForm, db: Session = Depends(get_db)):

    # Check if user exists
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.password):
            return {"status_code": f"{status.HTTP_400_BAD_REQUEST}", "detail": "Invalid username or password"}
    except Exception as es:
        print(es)
        return es

    # Generate token
    user.user_id = str(user.user_id)
    access_token = create_access_token(user)
    user_data = {
        "username": user.username,
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at,
        "is_active": user.is_active,
        "email": user.email,
        "role": user.role,
        "state": user.state,
        "city": user.city,
        "long": user.long,
        "lat": user.lat
    }
    await rabbitmq_service.publish_event(event_name="user.logs.in", data=user_data)
    # print({"access_token": access_token, "token_type": "Bearer", "data": user_data})
    return {"access_token": access_token, "token_type": "Bearer", "data": user_data}

    
@app.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: dict, db: Session = Depends(get_db)):
    has_role(
        required_roles=[UserRole.DONOR.value, UserRole.ADMIN.value,
                        UserRole.HOSPITAL_ADMIN.value, UserRole.REQUESTER.value,
                        UserRole.VOLUNTEER.value], user=user)
    user = db.query(User).filter(User.user_id == user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(user_id: str, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    # Extract decoded token

    decoded_token = body.get("user_dict")
    user_data = body.get("user_data")
    if not decoded_token:
            raise HTTPException(status_code=403, detail="Access Denied: No token provided")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Users can only update their own profile (unless an admin is modifying any user)
    if decoded_token["user_id"] != user.user_id and decoded_token["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Permission denied")

    user_obj = replace_val(update_data=user_data, user=user)
    # Update user fields
    stmt = sqlalchemy_update(User).where(User.user_id == user_id).values(**user_obj)
    try:
        db.execute(stmt)
        db.commit()
        db.refresh(user)
        await rabbitmq_service.publish_event(event_name="user.updated", data=user)
        return user
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another user is using the email you provided")

@app.get("", status_code=status.HTTP_200_OK, response_model=UserListResponse)
async def get_users(current_user: dict, db: Session = Depends(get_db)):
    has_role(
        required_roles=[UserRole.DONOR.value, UserRole.ADMIN.value,
                        UserRole.HOSPITAL_ADMIN.value, UserRole.REQUESTER.value,
                        UserRole.VOLUNTEER.value], user=current_user)

    users = db.query(User).all()
    return {"users": users}


@app.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(current_user: dict, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Users can only delete their own account (unless an admin is deleting any user)
    if current_user["user_id"] != user.user_id and current_user["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        db.delete(user)
        db.commit()
        await rabbitmq_service.publish_event(event_name="user.deleted", data=user)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
