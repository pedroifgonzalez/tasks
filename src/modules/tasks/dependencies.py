from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.modules.tasks.repository import TaskRepository
from src.modules.tasks.service import TaskService


async def get_task_repository(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db=db)


async def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository=repository)
