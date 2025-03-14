from fastapi import status, FastAPI
import uvicorn
from router import route


app = FastAPI(title="Lifeline Backend")
app.include_router(route.router)


@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return {
        "status": "I am Alive and runing"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

