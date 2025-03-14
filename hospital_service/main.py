from fastapi import FastAPI
import uvicorn

from route.hospital_router import app as hospital_route


app = FastAPI(title="Hospital Service Backend")

app.include_router(router=hospital_route)

@app.get("/")
async def home():
    return{
        "status": "I am Alive! What's up, from the hospital service!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
