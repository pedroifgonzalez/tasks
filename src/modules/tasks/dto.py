from pydantic import BaseModel, field_validator

from src.core.logging import logger
from src.modules.tasks.model import TaskStatus


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            logger.error("Title must not be empty")
            raise ValueError("Title must not be empty")
        return v


class CreateTask(TaskBase):
    title: str
    description: str | None = None


class UpdateTask(TaskBase):
    description: str | None = None
    status: TaskStatus | None = None
