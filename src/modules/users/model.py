from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import relationship

from src.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )
