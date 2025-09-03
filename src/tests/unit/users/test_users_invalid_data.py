import pytest
from httpx import AsyncClient

from src.modules.users.model import User


@pytest.mark.asyncio
async def test_sign_up_existent_email(db_user: User, client: AsyncClient):
    response = await client.post(
        "/users", json={"email": f"{db_user.email}", "password": "testpassword"}
    )
    assert response.status_code == 400
