from fastapi import Depends

from src.common.dependencies import get_auth_repository, get_user_repository
from src.modules.auth.repository import AuthRepository
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> UserService:
    return UserService(user_repository=user_repository, auth_repository=auth_repository)
