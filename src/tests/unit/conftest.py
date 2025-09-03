import logging
import os
import sys
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from httpx import AsyncClient
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from main import app
from src.core.config import settings
from src.db.base import Base
from src.db.session import get_db
from src.modules.auth.service import TokenPayload
from src.modules.users.model import User

# --- Database URL ---
db_url = os.getenv("DATABASE_URL", "").lower()
disable_logs = os.getenv("DISABLE_LOGS", "true").lower() in ["true", "1", "t"]

production_indicators = ["production", "prod", "live"]
if not db_url.strip() or any(ind in db_url for ind in production_indicators):
    print("❌ ERROR: Tests cannot run against a production database.")
    sys.exit(1)


TEST_USER_PASSWORD = "testuserpassword"


# --- Prepare database schema once per test session ---
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async_engine = create_async_engine(db_url, future=True, echo=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield  # Run all tests

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


# --- Create fresh DB + session per test ---
@pytest_asyncio.fixture(scope="function")
async def db():
    async_engine = create_async_engine(db_url, future=True, echo=False)
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()
    await async_engine.dispose()


# --- Cleanup tables between tests ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def cleanup_data(db: AsyncSession):
    for table in reversed(Base.metadata.sorted_tables):
        await db.execute(table.delete())
    await db.commit()
    yield
    for table in reversed(Base.metadata.sorted_tables):
        await db.execute(table.delete())
    await db.commit()


# --- Test Configuration ---


@pytest.fixture(autouse=disable_logs)
def disable_logging():
    """Disable logging during tests."""
    # Disable standard logging
    logging.disable(logging.CRITICAL)

    # Disable Loguru logs
    from loguru import logger

    # Remove all existing handlers
    logger.remove()

    # Add a null handler to suppress all logs
    null_handler = logger.add(lambda _: None, level="TRACE")

    yield

    # Re-enable standard logging
    logging.disable(logging.NOTSET)

    # Remove the null handler and re-add the default logging configuration
    logger.remove(null_handler)

    # Re-initialize logging with default configuration
    from src.core.logging import logger as app_logger

    app_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        level="DEBUG",
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )


# --- FastAPI test client ---
@pytest_asyncio.fixture(scope="function")
async def client(db: AsyncSession):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        # Try new httpx syntax first
        from httpx import ASGITransport

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test", follow_redirects=True
        ) as ac:
            yield ac
    except (ImportError, TypeError):
        # Fall back to old syntax
        async with AsyncClient(
            app=app, base_url="http://test", follow_redirects=True
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


# --- Helpers ---
def create_test_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = TokenPayload(id=user.id, email=user.email, exp=expire)
    token = jwt.encode(
        {**payload.model_dump(), "id": str(payload.id)},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


@pytest_asyncio.fixture(scope="function")
async def db_user(db: AsyncSession):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)
    hashed_password = pwd_context.hash(TEST_USER_PASSWORD)
    user = User(email="testuser@example.com", hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    yield user
