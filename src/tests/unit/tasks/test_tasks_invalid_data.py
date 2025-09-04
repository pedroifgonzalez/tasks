"""Assert that every task endpoint is protected by authentication and each user can only see their own tasks"""

import pytest
from httpx import AsyncClient

from src.modules.tasks.model import Task
from src.modules.users.model import User
from src.tests.unit.conftest import create_test_token


@pytest.mark.asyncio
async def test_create_task(db_user: User, client: AsyncClient):
    token = create_test_token(db_user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/tasks", json={"title": " "}, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_path_paramter_get_task(
    db_task: Task,
    client: AsyncClient,
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/tasks/12", headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_no_belongs_to_user_get_task(
    db_task: Task,
    another_db_task: Task,
    client: AsyncClient,
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(f"/tasks/{another_db_task.id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "property, new_value",
    [
        ("title", " "),
        ("status", "INVALID_STATUS"),
    ],
    ids=[
        "Empty task title",
        "Invalid task status",
    ],
)
@pytest.mark.asyncio
async def test_invalid_data_update_task(
    db_task: Task, client: AsyncClient, property: str, new_value: str
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.put(
        f"/tasks/{db_task.id}", json={property: new_value}, headers=headers
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_data_delete_task(db_task: Task, client: AsyncClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete("/tasks/12", headers=headers)
    assert response.status_code == 422
