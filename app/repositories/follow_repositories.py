from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User
from schemas import UserCreate
from app.core.security import hash_password


def create_user(db: Session, data: UserCreate) -> User:
    hashed_pw = hash_password(data.password)  # use passlib/bcrypt
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
    )
    db.add(user)  # Stage INSERT
    db.commit()  # Write to DB
    db.refresh(user)  # Reload — populates id, created_at, etc.
    return user


# 2


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)  # Fastest — uses primary key


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


# With filtering
def get_active_users(db: Session) -> list[User]:
    stmt = select(User).where(User.is_active == True)
    return db.execute(stmt).scalars().all()


# 3


def update_user(db: Session, user_id: int, data: UserUpdate) -> User | None:
    user = db.get(User, user_id)
    if not user:
        return None

    # model_dump(exclude_unset=True) only returns fields actually sent
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# 4


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
