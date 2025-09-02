from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.modules.tasks.model import TaskStatus


class ReadTask(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadTasks(BaseModel):
    tasks: list[ReadTask]
