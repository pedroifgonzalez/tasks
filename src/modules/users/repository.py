from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.modules.users.dto import UserDto
from src.modules.users.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserDto) -> User:
        db_user = self.db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="User already exists")
        db_user = User(email=user.email, hashed_password=user.hashed_password)
        self.db.add(db_user)
        self.db.commit()
        return db_user

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, id: UUID) -> User:
        db_user = self.db.get(User, id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def get_by_email(self, email: str) -> User:
        db_user = self.db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
