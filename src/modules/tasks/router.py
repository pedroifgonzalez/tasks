from uuid import UUID

from fastapi import APIRouter, Depends

from src.modules.auth.dependencies import get_current_user
from src.modules.tasks.dependencies import get_task_service
from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.schema import ReadTask
from src.modules.tasks.service import TaskService
from src.modules.users.model import User

router = APIRouter()


@router.post("/", response_model=ReadTask)
async def create_task(
    task: CreateTask,
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    return await tasks_service.create(user=user, task=task)


@router.get("/", response_model=list[ReadTask])
async def get_tasks(
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    return await tasks_service.get_all(user=user)


@router.get("/{task_id}", response_model=ReadTask)
async def get_task(
    task_id: UUID,
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    return await tasks_service.get_by_id(user=user, task_id=task_id)


@router.put("/{task_id}", response_model=ReadTask)
async def update_task(
    task_id: UUID,
    task: UpdateTask,
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    return await tasks_service.update(user=user, task_id=task_id, task=task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    return await tasks_service.delete(user=user, task_id=task_id)
