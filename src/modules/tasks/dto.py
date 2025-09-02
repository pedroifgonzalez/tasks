from pydantic import BaseModel

from src.modules.tasks.model import TaskStatus


class CreateTask(BaseModel):
    title: str
    description: str | None = None
    user_id: str


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
