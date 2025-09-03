from uuid import UUID

from src.core.logging import audit
from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.repository import TaskRepository
from src.modules.tasks.schema import ReadTask
from src.modules.users.model import User


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create(self, user: User, task: CreateTask) -> ReadTask:
        db_task = self.repository.create(user_id=user.id, task=task)
        audit(f"Task with title {task.title} created for user {user.id}")
        return ReadTask.model_validate(db_task)

    def get_all(self, user: User) -> list[ReadTask]:
        audit(f"User {user.id} retrieved all its tasks")
        return [
            ReadTask.model_validate(task)
            for task in self.repository.get_all(user_id=user.id)
        ]

    def get_by_id(self, user: User, task_id: UUID) -> ReadTask:
        audit(f"User {user.id} retrieved task with id {task_id}")
        return ReadTask.model_validate(
            self.repository.get_by_id(user_id=user.id, id=task_id)
        )

    def update(self, user: User, task_id: UUID, task: UpdateTask) -> ReadTask:
        audit(f"User {user.id} updated task with id {task_id}")
        return ReadTask.model_validate(
            self.repository.update(user_id=user.id, id=task_id, task=task)
        )

    def delete(self, user: User, task_id: UUID) -> None:
        audit(f"User {user.id} deleted task with id {task_id}")
        self.repository.delete(user_id=user.id, id=task_id)
