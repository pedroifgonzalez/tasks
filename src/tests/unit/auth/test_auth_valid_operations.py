from fastapi.testclient import TestClient

from src.modules.users.model import User
from src.tests.unit.conftest import TEST_USER_PASSWORD


def test_login(db_user: User, client: TestClient):
    response = client.post(
        "/auth/login", json={"email": db_user.email, "password": TEST_USER_PASSWORD}
    )
    assert response.status_code == 200
