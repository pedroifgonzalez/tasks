from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.common.dependencies import get_auth_repository, get_user_repository
from src.modules.auth.repository import AuthRepository
from src.modules.auth.service import AuthService, token_auth_scheme
from src.modules.users.model import User
from src.modules.users.repository import UserRepository


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository, auth_repository=auth_repository)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme),
) -> User:
    return await auth_service.authenticate_user(token.credentials)
