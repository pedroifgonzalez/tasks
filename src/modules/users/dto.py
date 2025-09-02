from pydantic import BaseModel


class CreateUserDto(BaseModel):
    email: str
    hashed_password: str
