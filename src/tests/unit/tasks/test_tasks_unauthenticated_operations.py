"""Assert that all unauthenticated requests to each tasks endpoint returns forbidden responses"""

import pytest
from httpx import AsyncClient

from src.modules.tasks.model import Task


@pytest.mark.asyncio
async def test_unauthenticated_create_task(client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.post("/tasks", json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 403

    no_headers_response = await client.post("/tasks", json={"title": "Test Task"})
    assert no_headers_response.status_code == 403


@pytest.mark.asyncio
async def test_unauthenticated_get_tasks(db_task: Task, client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/tasks", headers=headers)
    assert response.status_code == 403

    no_headers_response = await client.get("/tasks")
    assert no_headers_response.status_code == 403


@pytest.mark.asyncio
async def test_unauthenticated_get_task(db_task: Task, client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 403

    no_headers_response = await client.get(f"/tasks/{db_task.id}")
    assert no_headers_response.status_code == 403


@pytest.mark.asyncio
async def test_unauthenticated_update_task(db_task: Task, client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.put(
        f"/tasks/{db_task.id}", json={"descrption": "New description"}, headers=headers
    )
    assert response.status_code == 403

    no_headers_response = await client.put(
        f"/tasks/{db_task.id}", json={"descrption": "New description"}, headers=headers
    )
    assert no_headers_response.status_code == 403


@pytest.mark.asyncio
async def test_delete_task(db_task: Task, client: AsyncClient):
    headers = {"Authorization": f"Bearer invalid_token"}
    response = await client.delete(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 403

    no_headers_response = await client.delete(f"/tasks/{db_task.id}", headers=headers)
    assert no_headers_response.status_code == 403
