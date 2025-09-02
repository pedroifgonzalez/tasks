from fastapi import APIRouter, Depends

from src.modules.tasks.dependencies import get_task_service
from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.schema import ReadTask
from src.modules.tasks.service import TaskService

router = APIRouter()


@router.post("/", response_model=ReadTask)
def create_task(
    task: CreateTask, tasks_service: TaskService = Depends(get_task_service)
):
    return tasks_service.create(task)


@router.get("/", response_model=list[ReadTask])
def get_tasks(tasks_service: TaskService = Depends(get_task_service)):
    return tasks_service.get_all()


@router.get("/{task_id}", response_model=ReadTask)
def get_task(task_id: str, tasks_service: TaskService = Depends(get_task_service)):
    return tasks_service.get_by_id(task_id)


@router.put("/{task_id}", response_model=ReadTask)
def update_task(
    task_id: str,
    task: UpdateTask,
    tasks_service: TaskService = Depends(get_task_service),
):
    return tasks_service.update(task_id, task)


@router.delete("/{task_id}")
def delete_task(task_id: str, tasks_service: TaskService = Depends(get_task_service)):
    return tasks_service.delete(task_id)
