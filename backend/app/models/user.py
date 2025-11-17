from datetime import datetime
from typing import List

from sqlalchemy import func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.db import Base
from app.schemas.user import UserRoleEnum


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=False)
    update_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=None
    )
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.user
    )
    last_login: Mapped[datetime] = mapped_column(
        nullable=True, default=None
    )

User.sessions = relationship(
    "UserSession", 
    back_populates="user",
    cascade="all, delete-orphan"
)
