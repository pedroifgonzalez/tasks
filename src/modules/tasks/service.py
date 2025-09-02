from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.repository import TaskRepository
from src.modules.tasks.schema import ReadTask


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create(self, task: CreateTask) -> ReadTask:
        db_task = self.repository.create(task)
        return ReadTask.model_validate(db_task)

    def get_all(self) -> list[ReadTask]:
        return [ReadTask.model_validate(task) for task in self.repository.get_all()]

    def get_by_id(self, task_id: str) -> ReadTask:
        return ReadTask.model_validate(self.repository.get_by_id(task_id))

    def update(self, task_id: str, task: UpdateTask) -> ReadTask:
        return ReadTask.model_validate(self.repository.update(task_id, task))

    def delete(self, task_id: str) -> None:
        self.repository.delete(task_id)
