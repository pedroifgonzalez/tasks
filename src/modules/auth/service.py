from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi.security import HTTPBearer
from jose import jwt
from pydantic.main import BaseModel
from starlette.exceptions import HTTPException

from src.core.config import settings
from src.modules.users.model import User
from src.modules.users.repository import UserRepository

token_auth_scheme = HTTPBearer()


class TokenPayload(BaseModel):
    id: UUID
    email: str
    exp: Optional[datetime]


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_access_token(
        self, data: TokenPayload, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token containing the given data.

        If expires_delta is given, the token will expire after that time.
        Otherwise, the token will expire after the default expiration time
        given by the JWT_ACCESS_TOKEN_EXPIRE_MINUTES setting.

        Args:
            data (dict): The data to encode in the token.
            expires_delta (timedelta, optional): The time until the token expires.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.model_copy() if data.exp is None else data
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.exp = expire
        encoded_jwt = jwt.encode(
            {**to_encode.model_dump(), "id": str(to_encode.id)},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> TokenPayload:
        """
        Decode token to get user-related data. Used for authentication.

        Args:
            token (str): Token to be decoded

        Returns:
            TokenPayload: Token data
        """
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            token_payload = TokenPayload(
                id=payload["id"], email=payload["email"], exp=payload["exp"]
            )
        except Exception:
            raise HTTPException(403, "Invalid token")
        return token_payload

    def authenticate_user(self, credentials: str) -> User:
        """
        Authenticates a user based on credentials validation

        Args:
            credentials (str): Expected encoded data string

        Returns:
            User: user authenticated

        Raises:
            HTTPException: in case the credentials can not be validated or the user id
            is not found
        """
        data = self.decode_access_token(credentials)
        user = self.repository.get_by_id(id=data.id)
        return user
