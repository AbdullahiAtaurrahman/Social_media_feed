from fastapi import FastAPI
from core.config import settings

from api.v1.users import router as users_router
from api.v1.posts import router as posts_router
from api.v1.comments import router as comments_router
from api.v1.comments import router as comments_router

from app.core.db import engine
from app.models import user  # ensures tables are registered
from app.models.users import User  # noqa — triggers Base.metadata
from app.core.db import Base
from app.api.v1 import auth, users

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
