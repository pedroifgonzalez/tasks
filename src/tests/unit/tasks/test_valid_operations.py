"""Assert that every task endpoint is protected by authentication and each user can only see their own tasks"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.modules.tasks.model import Task
from src.modules.users.model import User
from src.tests.unit.tasks.conftest import create_test_token


def test_create_task(db_user: User, db: Session, client: TestClient):
    token = create_test_token(db_user)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks", json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert len(db.query(Task).filter(Task.user_id == db_user.id).all()) == 1


def test_get_tasks(db_task: Task, another_db_task, db: Session, client: TestClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(db.query(Task).all()) == 2


def test_get_task(db_task: Task, client: TestClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    for prop in ["created_at", "id"]:
        data.pop(prop)
    assert data == {
        "title": "Test Task",
        "description": "Test Task Description",
        "status": "PENDING",
    }


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
def test_update_task(db_task: Task, client: TestClient, property: str, new_value: str):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        f"/tasks/{db_task.id}", json={property: new_value}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()[property] == new_value


def test_delete_task(db_task: Task, client: TestClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/tasks/{db_task.id}", headers=headers)
    assert response.status_code == 200
