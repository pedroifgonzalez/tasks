from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging import logger
from src.modules.users.dto import UserDto
from src.modules.users.model import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserDto) -> User:
        result = await self.db.execute(select(User).where(User.email == user.email))
        db_user = result.scalar_one_or_none()

        if db_user:
            logger.error(f"User with email {user.email} already exists")
            raise HTTPException(status_code=400, detail="User already exists")

        db_user = User(email=user.email, hashed_password=user.hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def get_by_id(self, id: UUID) -> User:
        db_user = await self.db.get(User, id)
        if not db_user:
            logger.error(f"User with id {id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    async def get_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        db_user = result.scalar_one_or_none()

        if not db_user:
            logger.error(f"User with email {email} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
