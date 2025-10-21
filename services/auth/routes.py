from fastapi import APIRouter, HTTPException
from .schemas import UserCreate, UserOut
from .crud import get_user_by_email, create_user
from .security import hash_password, create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User exists")
    hashed = hash_password(user.password)
    new_user = await create_user(user.email, hashed)
    if not new_user:
        raise HTTPException(status_code=500, detail="Error creating user")
    return new_user

@router.post("/login")
async def login(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/ping")
async def ping():
    return {"status": "ok"}
