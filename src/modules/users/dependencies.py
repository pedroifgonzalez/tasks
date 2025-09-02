from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository=repository)
