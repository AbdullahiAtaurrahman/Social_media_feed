from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Router inclusion is intentionally deferred until the feature modules are cleaned up.
# from app.api.v1.users import router as users_router
# from app.api.v1.posts import router as posts_router
# from app.api.v1.comments import router as comments_router
# app.include_router(users_router, prefix=settings.API_V1_STR)
# app.include_router(posts_router, prefix=settings.API_V1_STR)
# app.include_router(comments_router, prefix=settings.API_V1_STR)
