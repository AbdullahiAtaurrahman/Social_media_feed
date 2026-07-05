from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media Feed"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "DEBUG"  # DEBUG | STAGING | PRODUCTION

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Redis
    REDIS_URL: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL_ASYNC: str
    DATABASE_URL: str

    celery_broker_url: str
    celery_result_backend: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@property
def is_debug(self) -> bool:
    return self.ENVIRONMENT == "debug"


@property
def is_production(self) -> bool:
    return self.ENVIRONMENT == "production"


settings = Settings()
