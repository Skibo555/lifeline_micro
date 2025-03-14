from fastapi import APIRouter


from server import router


app = APIRouter()

app.include_router(router)
