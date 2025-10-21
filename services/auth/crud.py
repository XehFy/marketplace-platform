from sqlalchemy import select
from .models import User
from .database import async_session
from sqlalchemy.exc import IntegrityError

async def get_user_by_email(email: str) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

async def create_user(email: str, hashed_password: str):
    async with async_session() as session:
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError:
            await session.rollback()
            return None
