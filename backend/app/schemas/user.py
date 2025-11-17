from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from enum import Enum
from datetime import datetime

class UserRoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    hardware = "hardware"

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRoleEnum = UserRoleEnum.user


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserAllow(BaseModel):
    is_active: bool
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserDetail(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRoleEnum
    is_active: bool
    created_at: datetime
    update_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserDetail]


class UserStats(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    users_by_role: dict
    recent_logins: int 
    active_sessions: int
    total_sessions_today: int
    unique_users_today: int
    average_session_duration: float
