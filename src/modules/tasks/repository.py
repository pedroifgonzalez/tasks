from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging import logger
from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.model import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, task: CreateTask) -> Task:
        """Create a new task.

        Args:
            user_id (UUID): The user owner ID of the task.
            task (CreateTask): The task to create.

        Returns:
            Task: The created task.

        Raises:
            HTTPException: If the task already exists.

        """
        result = await self.db.execute(
            select(Task).where(Task.title == task.title, Task.user_id == user_id)
        )
        db_task = result.scalar_one_or_none()

        if db_task:
            logger.error(f"There is a task with the same title {task.title}")
            raise HTTPException(status_code=400, detail="Task already exists")

        db_task = Task(title=task.title, description=task.description, user_id=user_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_all(
        self, user_id: UUID, page: int, page_size: int
    ) -> tuple[list[Task], int]:
        """Get all tasks.

        Args:
            user_id (UUID): The user owner ID of the task.
            page (int): The page number.
            page_size (int): The number of tasks per page.

        Returns:
            list[Task]: The list of tasks.
            total[int]: The total number of tasks.

        """
        query = select(Task).where(Task.user_id == user_id)
        result = await self.db.execute(
            query.offset((page - 1) * page_size).limit(page_size)
        )
        total = await self.db.execute(
            select(func.count()).select_from(Task).where(Task.user_id == user_id)
        )
        paginated_tasks = result.scalars().all()
        return list(paginated_tasks), total.scalar_one()

    async def get_by_id(self, user_id: UUID, id: UUID) -> Task | None:
        """Get a task by id.

        Args:
            user_id (UUID): The id of the authenticated user
            id (UUID): The id of the task.

        Returns:
            Task: The task.

        Raises:
            HTTPException: If the task is not found.

        """
        result = await self.db.execute(
            select(Task).where(Task.id == id, Task.user_id == user_id)
        )
        db_task = result.scalar_one_or_none()

        if not db_task:
            logger.error(f"Task with id {id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task

    async def update(self, id: UUID, user_id: UUID, task: UpdateTask) -> Task:
        """Update a task.

        Args:
            id (UUID): The id of the task.
            user_id (UUID): The id of the authenticated user
            task (UpdateTask): The task to update.

        Returns:
            Task: The updated task.

        Raises:
            HTTPException: If the task is not found.

        """
        db_task = await self.get_by_id(id=id, user_id=user_id)
        if not db_task:
            logger.error(f"Task with id {id} not found")
            raise HTTPException(status_code=404, detail="Task not found")

        if task.title is not None:
            db_task.title = task.title
        if task.description is not None:
            db_task.description = task.description
        if task.status is not None:
            db_task.status = task.status

        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete(self, user_id: UUID, id: UUID):
        """Delete a task.

        Args:
            user_id (UUID): The id of the authenticated user
            id (str): The id of the task.

        Returns:
            Task: The deleted task.

        Raises:
            HTTPException: If the task is not found.

        """
        db_task = await self.get_by_id(id=id, user_id=user_id)
        if not db_task:
            logger.error(f"Task with id {id} not found")
            raise HTTPException(status_code=404, detail="Task not found")

        await self.db.delete(db_task)
        await self.db.commit()
        return db_task
