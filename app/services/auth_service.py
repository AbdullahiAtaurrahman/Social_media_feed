from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.schemas.auth import Token
from app.schemas.users import UserCreate
from app.models.users import User


class AuthService:
    @staticmethod
    def register(db: Session, data: UserCreate) -> User:
        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(status_code=400, detail="Username already taken")
        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        return UserRepository.create(db, data)

    @staticmethod
    def login(db: Session, username: str, password: str) -> Token:
        user = UserRepository.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_access_token(
            data={"sub": user.username, "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return Token(access_token=token, token_type="bearer")
