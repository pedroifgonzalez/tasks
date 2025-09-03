import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.tasks.model import Task
from src.modules.users.model import User
from src.tests.unit.conftest import create_test_token


@pytest.mark.asyncio
async def test_create_task(db_user: User, db: AsyncSession, client: AsyncClient):
    token = create_test_token(db_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/tasks", json={"title": "Test Task"}, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

    result = await db.execute(select(Task).filter(Task.user_id == db_user.id))
    tasks = result.scalars().all()
    assert len(tasks) == 1


@pytest.mark.asyncio
async def test_get_tasks(
    db_task: Task, another_db_task: Task, db: AsyncSession, client: AsyncClient
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/tasks", headers=headers)

    assert response.status_code == 200
    assert len(response.json().get("items")) == 1  # only owner sees their own tasks

    result = await db.execute(select(Task))
    all_tasks = result.scalars().all()
    assert len(all_tasks) == 2  # two tasks in DB, but only one visible to user


@pytest.mark.asyncio
async def test_get_task(db_task: Task, client: AsyncClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"/tasks/{db_task.id}", headers=headers)

    assert response.status_code == 200
    data = response.json()

    # Ignore dynamic props
    for prop in ["created_at", "id"]:
        data.pop(prop)

    assert data == {
        "title": "Test Task",
        "description": "Test Task Description",
        "status": "PENDING",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "property, new_value",
    [
        ("title", "New Title Task"),
        ("description", "Add a description"),
        ("status", "COMPLETED"),
    ],
    ids=[
        "Update task title",
        "Update task description",
        "Update task status",
    ],
)
async def test_update_task(
    db_task: Task, client: AsyncClient, property: str, new_value: str
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.put(
        f"/tasks/{db_task.id}", json={property: new_value}, headers=headers
    )

    assert response.status_code == 200
    assert response.json()[property] == new_value


@pytest.mark.asyncio
async def test_delete_task(db_task: Task, client: AsyncClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.delete(f"/tasks/{db_task.id}", headers=headers)

    assert response.status_code == 200
