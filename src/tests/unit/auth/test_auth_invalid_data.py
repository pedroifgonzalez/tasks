from fastapi.testclient import TestClient

from src.modules.users.model import User


def test_invalid_password_login(db_user: User, client: TestClient):
    response = client.post(
        "/auth/login", json={"email": db_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 403


def test_nonexistent_email_login(db_user: User, client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 403
