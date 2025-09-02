import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.modules.tasks.model import Task
from src.modules.users.model import User


def test_create_task(db_user: User, db: Session, client: TestClient):
    response = client.post("/tasks", json={"title": "Test Task", "user_id": db_user.id})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_tasks(db_task: Task, db: Session, client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "task_id, expected_data, ignore_attributes, expected_status",
    [
        (
            "550e8400-e29b-41d4-a716-446655440000",
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Test Task",
                "description": "Test Task Description",
                "status": "PENDING",
            },
            ["created_at"],
            200,
        ),
        ("550e8400-e29b-41d4-a719-476855440000", None, None, 404),
    ],
)
def test_get_task(
    db_task: Task,
    db: Session,
    client: TestClient,
    task_id: str,
    expected_status: int,
    expected_data: dict,
    ignore_attributes: list[str] | None,
):
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == expected_status
    if expected_data:
        for k, _ in response.json().items():
            if k in ignore_attributes:
                continue
            assert response.json()[k] == expected_data[k]


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
def test_update_task(
    db_task: Task, db: Session, client: TestClient, property: str, new_value: str
):
    response = client.put(f"/tasks/{db_task.id}", json={property: new_value})
    assert response.status_code == 200
    assert response.json()[property] == new_value


@pytest.mark.parametrize(
    "task_id, expected_status",
    [
        ("550e8400-e29b-41d4-a716-446655440000", 200),
        ("550e8400-e29b-41d4-a719-476855440000", 404),
    ],
)
def test_delete_task(
    db_task: Task, db: Session, client: TestClient, task_id: str, expected_status: int
):
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == expected_status
