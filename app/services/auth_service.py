from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.schemas.auth import Token
from app.schemas.users import UserCreate
from app.models.users import User


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, data: UserCreate) -> User:
        if await UserRepository.get_by_username(db, data.username):
            raise HTTPException(status_code=400, detail="Username already taken")
        if await UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        return await UserRepository.create_user(db, data)

    @staticmethod
    async def login(db: Session, username: str, password: str) -> Token:
        user = await UserRepository.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            raise await HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_access_token(
            data={"sub": user.username, "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return await Token(access_token=token, token_type="bearer")
