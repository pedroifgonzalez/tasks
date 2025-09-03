from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.modules.auth.repository import AuthRepository
from src.modules.users.repository import UserRepository


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


async def get_auth_repository() -> AuthRepository:
    return AuthRepository()
