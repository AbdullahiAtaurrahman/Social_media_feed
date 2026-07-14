from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

from app.api.v1.posts import router as posts_router

app.include_router(posts_router, prefix=settings.API_V1_STR)
