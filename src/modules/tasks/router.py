from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.common.pagination import PaginatedResponse
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


@router.get("/", response_model=PaginatedResponse[ReadTask])
async def get_tasks(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page (max 100)"
    ),
    tasks_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
):
    tasks, total = await tasks_service.get_all(
        user=user, page=page, page_size=page_size
    )
    return PaginatedResponse.create(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size,
    )


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
