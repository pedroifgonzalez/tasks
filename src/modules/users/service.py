from src.modules.users.dto import CreateUserDto
from src.modules.users.model import User
from src.modules.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, user: CreateUserDto) -> User:
        return self.repository.create(user)

    def get_all(self) -> list[User]:
        return self.repository.get_all()
