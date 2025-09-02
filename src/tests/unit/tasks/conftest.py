import pytest
from sqlalchemy.orm import Session

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
        id="550e8400-e29b-41d4-a716-446655440000",
    )
    db.add(db_task)
    db.commit()
    yield db_task
