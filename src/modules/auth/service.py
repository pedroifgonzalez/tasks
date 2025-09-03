from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext
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
        self.pwd_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10
        )

    def get_password_hash(self, password: str) -> str:
        """
        Hash the given plain password and return the hashed string.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password string.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify that the given plain password matches the given hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

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
        data = self.decode_access_token(credentials)
        user = self.repository.get_by_id(id=data.id)
        return user
