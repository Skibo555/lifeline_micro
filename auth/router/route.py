from fastapi import APIRouter

from controller.user_auth import app
from controller.hospital_management import router as hospital_router

router = APIRouter()

router.include_router(app)
# router.include_router(hospital_router)


