"""User business logic."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import get_password_hash

class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
            
        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")
            
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

user_service = UserService()
