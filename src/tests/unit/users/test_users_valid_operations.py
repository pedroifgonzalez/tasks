import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.model import User


@pytest.mark.asyncio
async def test_sign_up(db: AsyncSession, client: AsyncClient):
    response = await client.post(
        "/users", json={"email": "testuser@gmail.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    result = await db.execute(select(User))
    all_users = result.scalars().all()
    assert len(all_users) == 1
    db_user = all_users[0]
    assert db_user is not None
    assert db_user.email == "testuser@gmail.com"
