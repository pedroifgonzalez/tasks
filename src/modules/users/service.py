from src.core.logging import audit
from src.modules.auth.repository import AuthRepository
from src.modules.users.dto import CreateUser, UserDto
from src.modules.users.model import User
from src.modules.users.repository import UserRepository


class UserService:
    def __init__(
        self, user_repository: UserRepository, auth_repository: AuthRepository
    ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    async def create(self, user: CreateUser) -> User:
        audit(f"User {user.email} created")
        hashed_password = await self.auth_repository.get_password_hash(
            password=user.password
        )
        user_dto = UserDto(email=user.email, hashed_password=hashed_password)
        return await self.user_repository.create(user_dto)

    async def get_all(self) -> list[User]:
        audit("All users retrieved")
        return await self.user_repository.get_all()
