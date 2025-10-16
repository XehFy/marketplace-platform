from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/ping")
async def ping_auth():
    return {"status": "ok", "service": "auth"}
