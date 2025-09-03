import pytest
from httpx import AsyncClient

from src.modules.users.model import User
from src.tests.unit.conftest import TEST_USER_PASSWORD


@pytest.mark.asyncio
async def test_login(db_user: User, client: AsyncClient):
    response = await client.post(
        "/auth/login", json={"email": db_user.email, "password": TEST_USER_PASSWORD}
    )
    assert response.status_code == 200
