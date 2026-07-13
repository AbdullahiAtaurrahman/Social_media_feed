from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media Feed"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "DEBUG"  # DEBUG | STAGING | PRODUCTION

    # Auth
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URL_ASYNC: str
    DATABASE_URL: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@property
def is_debug(self) -> bool:
    return self.ENVIRONMENT == "DEBUG"


@property
def is_production(self) -> bool:
    return self.ENVIRONMENT == "PRODUCTION"


settings = Settings()
