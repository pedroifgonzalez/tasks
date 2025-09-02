from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.tasks.repository import TaskRepository
from src.modules.tasks.service import TaskService


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db=db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository=repository)
