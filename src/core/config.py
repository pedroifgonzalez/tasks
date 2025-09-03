import multiprocessing
import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # JWT settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"

    # Concurrency settings
    WORKERS_COUNT: int = multiprocessing.cpu_count() * 2 + 1
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"

    # Database pool settings
    DB_POOL_SIZE: int = multiprocessing.cpu_count() * 5
    DB_MAX_OVERFLOW: int = multiprocessing.cpu_count() * 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes


# Load settings from environment variables
settings = Settings()  # pydantic-settings automatically loads from .env
