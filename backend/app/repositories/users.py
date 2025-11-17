from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from datetime import datetime, timedelta, timezone

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = await self.session.get(User, user_id)
        return stmt

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = await self.session.scalars(stmt)
        return result.first()

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all_users_repository(self) -> list[User]:
        stmt = select(User)
        result = await self.session.scalars(stmt)
        return result.all()

    async def delete_user(self, user_id: int):
        user = await self.session.get(User, user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

    async def get_user_stats(self) -> dict:
        # Total
        total_stmt = select(func.count(User.id))
        total_result = await self.session.execute(total_stmt)
        total_users = total_result.scalar()

        # active
        active_stmt = select(func.count(User.id)).where(User.is_active == True)
        active_result = await self.session.execute(active_stmt)
        active_users = active_result.scalar()

        # inactive
        inactive_users = total_users - active_users

        # by role
        role_stmt = select(User.role, func.count(User.id)).group_by(User.role)
        role_result = await self.session.execute(role_stmt)
        users_by_role = {role.value: count for role, count in role_result.fetchall()}

        # recent logins (24h)
        yesterday = datetime.now() - timedelta(days=1)
        recent_stmt = select(func.count(User.id)).where(User.last_login >= yesterday)
        recent_result = await self.session.execute(recent_stmt)
        recent_logins = recent_result.scalar()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "users_by_role": users_by_role,
            "recent_logins": recent_logins,
        }

    async def update_last_login(self, user: User):
        user.last_login = datetime.now(timezone.utc)
        await self.update_user(user)
