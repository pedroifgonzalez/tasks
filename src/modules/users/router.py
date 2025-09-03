from fastapi import APIRouter, Depends

from src.modules.users.dependencies import get_user_service
from src.modules.users.dto import CreateUser
from src.modules.users.service import UserService

router = APIRouter()


@router.post("/")
def sign_up(user: CreateUser, user_service: UserService = Depends(get_user_service)):
    return user_service.create(user)
