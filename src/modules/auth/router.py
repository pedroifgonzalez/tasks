from fastapi import APIRouter, Depends

from src.modules.auth.dependencies import get_auth_service
from src.modules.auth.service import AuthService
from src.modules.users.dto import CreateUser as LoginUser

router = APIRouter()


@router.post("/login")
def login(user_data: LoginUser, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login_user(user_data=user_data)
