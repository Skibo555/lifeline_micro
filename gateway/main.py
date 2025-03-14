from fastapi import FastAPI, status, Request, HTTPException

import uvicorn

from router.router import routes

app = FastAPI()
app.include_router(router=routes)


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {
        "status": "Gateway is Alive!"
    }

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8088, reload=True)

