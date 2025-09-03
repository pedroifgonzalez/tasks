from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.service import AuthService, token_auth_scheme
from src.modules.users.model import User
from src.modules.users.repository import UserRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repository=repository)


def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme),
) -> User:
    return auth_service.authenticate_user(token.credentials)
