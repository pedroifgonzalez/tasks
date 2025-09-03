from fastapi.testclient import TestClient

from src.modules.users.model import User


def test_sign_up_existent_email(db_user: User, client: TestClient):
    response = client.post(
        "/users", json={"email": f"{db_user.email}", "password": "testpassword"}
    )
    assert response.status_code == 400
