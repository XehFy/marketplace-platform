from fastapi import FastAPI
from .routes import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router)

@app.get("/ping")
async def ping():
    return {"message": "pong"}
