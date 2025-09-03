import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from main import app
from src.core.config import settings
from src.db.base import Base
from src.db.session import get_db
from src.modules.auth.service import TokenPayload
from src.modules.users.model import User

db_url = os.getenv("DATABASE_URL", "").lower()

# Block production DBs
production_indicators = ["production", "prod", "live"]
if not db_url.strip() or any(
    indicator in db_url for indicator in production_indicators
):
    print("ERROR: Tests cannot run against a production database. Aborting.")
    sys.exit(1)

# Test engine and session
engine = create_engine(db_url, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once per test session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Provide a transactional scope around each test."""
    session: Session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function", autouse=True)
def cleanup_data(db: Session):
    """Ensure tables are cleared between tests."""
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


@pytest.fixture(scope="function")
def client(db: Session):
    """FastAPI test client with overridden DB dependency."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def create_test_token(user: User) -> str:
    """Create a test JWT token for authentication."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = TokenPayload(id=user.id, email=user.email, exp=expire)
    token = jwt.encode(
        {**payload.model_dump(), "id": str(payload.id)},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


@pytest.fixture(scope="function")
def db_user(db: Session):
    user = User(email="testuser@example.com", hashed_password="test")
    db.add(user)
    db.commit()
    yield user
