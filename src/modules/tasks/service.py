from uuid import UUID

from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.repository import TaskRepository
from src.modules.tasks.schema import ReadTask
from src.modules.users.model import User


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create(self, user: User, task: CreateTask) -> ReadTask:
        db_task = self.repository.create(user_id=user.id, task=task)
        return ReadTask.model_validate(db_task)

    def get_all(self, user: User) -> list[ReadTask]:
        return [
            ReadTask.model_validate(task)
            for task in self.repository.get_all(user_id=user.id)
        ]

    def get_by_id(self, user: User, task_id: UUID) -> ReadTask:
        return ReadTask.model_validate(
            self.repository.get_by_id(user_id=user.id, id=task_id)
        )

    def update(self, user: User, task_id: UUID, task: UpdateTask) -> ReadTask:
        return ReadTask.model_validate(
            self.repository.update(user_id=user.id, id=task_id, task=task)
        )

    def delete(self, user: User, task_id: UUID) -> None:
        self.repository.delete(user_id=user.id, id=task_id)
