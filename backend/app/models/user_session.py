from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.db import Base


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    session_token: Mapped[str] = mapped_column(unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=True)
    device_info: Mapped[str] = mapped_column(nullable=True)
    ip_address: Mapped[str] = mapped_column(nullable=True)
    user_agent: Mapped[str] = mapped_column(nullable=True)
    login_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=None
    )
    last_activity: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
        default=None
    )
    logout_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    expires_at: Mapped[datetime] = mapped_column(nullable=False, default=None)
    is_active: Mapped[bool] = mapped_column(default=True)
    
UserSession.user = relationship("User", back_populates="sessions")
