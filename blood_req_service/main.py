from fastapi import FastAPI
import uvicorn

from router.route import app as request_router


app = FastAPI(title="Request Service")
app.include_router(request_router)


@app.get("/")
async def home():
    message = {
        "message": "Request service is alive!"
    }
    return message


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8989, reload=True)

