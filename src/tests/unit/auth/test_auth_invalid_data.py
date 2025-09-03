import pytest
from httpx import AsyncClient

from src.modules.users.model import User


@pytest.mark.asyncio
async def test_invalid_password_login(db_user: User, client: AsyncClient):
    response = await client.post(
        "/auth/login", json={"email": db_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_nonexistent_email_login(db_user: User, client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 403
