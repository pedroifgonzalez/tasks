from uuid import uuid4

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.tasks.model import Task
from src.modules.users.model import User


@pytest_asyncio.fixture(scope="function")
async def db_task(db: AsyncSession, db_user: User):
    db_task = Task(
        title="Test Task",
        user_id=db_user.id,
        description="Test Task Description",
        id=uuid4(),
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    yield db_task


@pytest_asyncio.fixture(scope="function")
async def another_db_user(db: AsyncSession):
    user = User(email="another_db_user@example.com", hashed_password="test")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    yield user


@pytest_asyncio.fixture(scope="function")
async def another_db_task(db: AsyncSession, another_db_user: User):
    db_task = Task(
        title="Another Test Task",
        user_id=another_db_user.id,
        description="Another Test Task Description",
        id=uuid4(),
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    yield db_task
