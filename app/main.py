from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import TimingMiddleware


from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.middleware(
    CORSMiddleware(
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)

app.add_middleware(TimingMiddleware)


from app.api.v1.posts import router as posts_router

app.include_router(posts_router, prefix=settings.API_V1_STR)
