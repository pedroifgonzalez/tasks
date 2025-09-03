from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str


class UserDto(BaseModel):
    email: str
    hashed_password: str
