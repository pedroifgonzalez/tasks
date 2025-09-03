from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.repository import AuthRepository
from src.modules.users.repository import UserRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_auth_repository() -> AuthRepository:
    return AuthRepository()
