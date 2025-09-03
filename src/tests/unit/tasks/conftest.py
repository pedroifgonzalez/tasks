from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from jose import jwt
from sqlalchemy.orm import Session

from src.core.config import settings
from src.modules.auth.service import TokenPayload
from src.modules.tasks.model import Task
from src.modules.users.model import User


@pytest.fixture(scope="function")
def db_user(db: Session):
    user = User(email="testuser@example.com", hashed_password="test")
    db.add(user)
    db.commit()
    yield user


@pytest.fixture(scope="function")
def db_task(db: Session, db_user: User):
    db_task = Task(
        title="Test Task",
        user_id=db_user.id,
        description="Test Task Description",
        id=uuid4(),
    )
    db.add(db_task)
    db.commit()
    yield db_task


@pytest.fixture(scope="function")
def another_db_user(db: Session):
    user = User(email="another_db_user@example.com", hashed_password="test")
    db.add(user)
    db.commit()
    yield user


@pytest.fixture(scope="function")
def another_db_task(db: Session, another_db_user: User):
    db_task = Task(
        title="Another Test Task",
        user_id=another_db_user.id,
        description="Another Test Task Description",
        id=uuid4(),
    )
    db.add(db_task)
    db.commit()
    yield db_task


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
