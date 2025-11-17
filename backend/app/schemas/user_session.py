from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserSessionCreate(BaseModel):
    user_id: int
    session_token: str
    refresh_token: Optional[str] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    expires_at: datetime


class UserSessionUpdate(BaseModel):
    last_activity: Optional[datetime] = None
    logout_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class UserSessionResponse(BaseModel):
    id: int
    user_id: int
    session_token: str
    device_info: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    login_at: datetime
    last_activity: datetime
    logout_at: Optional[datetime]
    expires_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class SessionStats(BaseModel):
    active_sessions: int
    total_sessions_today: int
    unique_users_today: int
    average_session_duration: float  
    sessions_by_device: dict
