from fastapi import APIRouter

from user import server
from hospital import router
from request import router as request_router

routes = APIRouter()

routes.include_router(server)
routes.include_router(router)
routes.include_router(request_router)
