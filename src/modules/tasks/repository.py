from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.modules.tasks.dto import CreateTask, UpdateTask
from src.modules.tasks.model import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: CreateTask) -> Task:
        """Create a new task.

        Args:
            task (CreateTask): The task to create.

        Returns:
            Task: The created task.

        Raises:
            HTTPException: If the task already exists.

        """
        db_task = (
            self.db.query(Task)
            .filter(Task.title == task.title, Task.user_id == task.user_id)
            .first()
        )
        if db_task:
            raise HTTPException(status_code=400, detail="Task already exists")
        db_task = Task(
            title=task.title, description=task.description, user_id=task.user_id
        )
        self.db.add(db_task)
        self.db.commit()
        return db_task

    def get_all(self) -> list[Task]:
        """Get all tasks.

        Returns:
            list[Task]: The list of tasks.

        """
        return self.db.query(Task).all()

    def get_by_id(self, task_id: str) -> Task | None:
        """Get a task by id.

        Args:
            task_id (str): The id of the task.

        Returns:
            Task: The task.

        Raises:
            HTTPException: If the task is not found.

        """
        db_task = self.db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task

    def update(self, id: str, task: UpdateTask) -> Task:
        """Update a task.

        Args:
            id (str): The id of the task.
            task (UpdateTask): The task to update.

        Returns:
            Task: The updated task.

        Raises:
            HTTPException: If the task is not found.

        """
        db_task = self.get_by_id(id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.title is not None:
            db_task.title = task.title
        if task.description is not None:
            db_task.description = task.description
        if task.status is not None:
            db_task.status = task.status
        self.db.commit()
        return db_task

    def delete(self, id: str):
        """Delete a task.

        Args:
            id (str): The id of the task.

        Returns:
            Task: The deleted task.

        Raises:
            HTTPException: If the task is not found.

        """
        db_task = self.get_by_id(id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        self.db.delete(db_task)
        self.db.commit()
        return db_task
