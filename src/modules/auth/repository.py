from passlib.context import CryptContext


class AuthRepository:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10
        )

    async def get_password_hash(self, password: str) -> str:
        """
        Hash the given plain password and return the hashed string.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password string.
        """
        return self.pwd_context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify that the given plain password matches the given hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
