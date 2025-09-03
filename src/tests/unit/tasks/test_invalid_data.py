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
    response = client.post("/tasks", json={"title": " "}, headers=headers)
    assert response.status_code == 422


def test_get_task(
    db_task: Task,
    db: Session,
    client: TestClient,
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/12", headers=headers)
    assert response.status_code == 422


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
def test_invalid_data_update_task(
    db_task: Task, db: Session, client: TestClient, property: str, new_value: str
):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        f"/tasks/{db_task.id}", json={property: new_value}, headers=headers
    )
    assert response.status_code == 422


def test_invalid_data_delete_task(db_task: Task, db: Session, client: TestClient):
    token = create_test_token(db_task.owner)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/tasks/12", headers=headers)
    assert response.status_code == 422
