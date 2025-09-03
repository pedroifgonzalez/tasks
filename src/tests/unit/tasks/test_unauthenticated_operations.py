"""Assert that all unauthenticated requests to each tasks endpoint returns forbidden responses"""

from fastapi.testclient import TestClient

from src.modules.tasks.model import Task


def test_unauthenticated_create_task(client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/tasks", json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 403

    no_headers_response = client.post("/tasks", json={"title": "Test Task"})
    assert no_headers_response.status_code == 403


def test_unauthenticated_get_tasks(db_task: Task, client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 403

    no_headers_response = client.get("/tasks")
    assert no_headers_response.status_code == 403


def test_unauthenticated_get_task(db_task: Task, client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 403

    no_headers_response = client.get(f"/tasks/{db_task.id}")
    assert no_headers_response.status_code == 403


def test_unauthenticated_update_task(db_task: Task, client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.put(
        f"/tasks/{db_task.id}", json={"descrption": "New description"}, headers=headers
    )
    assert response.status_code == 403

    no_headers_response = client.put(
        f"/tasks/{db_task.id}", json={"descrption": "New description"}, headers=headers
    )
    assert no_headers_response.status_code == 403


def test_delete_task(db_task: Task, client: TestClient):
    headers = {"Authorization": f"Bearer invalid_token"}
    response = client.delete(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 403

    no_headers_response = client.delete(f"/tasks/{db_task.id}", headers=headers)
    assert no_headers_response.status_code == 403
