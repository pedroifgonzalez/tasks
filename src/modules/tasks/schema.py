from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.modules.tasks.model import TaskStatus


class ReadTask(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadTasks(BaseModel):
    tasks: list[ReadTask]
