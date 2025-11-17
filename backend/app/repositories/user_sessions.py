from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, and_, or_
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from app.models.user_session import UserSession
from app.models.user import User


class UserSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, session_data: dict) -> UserSession:
        """Cria uma nova sessão de usuário"""
        user_session = UserSession(**session_data)
        self.session.add(user_session)
        await self.session.commit()
        await self.session.refresh(user_session)
        return user_session

    async def get_session_by_token(self, session_token: str) -> Optional[UserSession]:
        """Busca sessão por token"""
        stmt = select(UserSession).where(
            and_(
                UserSession.session_token == session_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_session_by_refresh_token(self, refresh_token: str) -> Optional[UserSession]:
        """Busca sessão por refresh token"""
        stmt = select(UserSession).where(
            and_(
                UserSession.refresh_token == refresh_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_session_activity(self, session_id: int) -> Optional[UserSession]:
        """Atualiza a última atividade da sessão"""
        stmt = select(UserSession).where(UserSession.id == session_id)
        result = await self.session.execute(stmt)
        user_session = result.scalar_one_or_none()
        
        if user_session:
            user_session.last_activity = datetime.now(timezone.utc)
            await self.session.commit()
            await self.session.refresh(user_session)
        
        return user_session

    async def logout_session(self, session_token: str) -> bool:
        """Faz logout de uma sessão específica"""
        stmt = select(UserSession).where(UserSession.session_token == session_token)
        result = await self.session.execute(stmt)
        user_session = result.scalar_one_or_none()
        
        if user_session:
            user_session.is_active = False
            user_session.logout_at = datetime.now(timezone.utc)
            await self.session.commit()
            return True
        
        return False

    async def logout_all_user_sessions(self, user_id: int) -> int:
        """Faz logout de todas as sessões de um usuário"""
        stmt = select(UserSession).where(
            and_(
                UserSession.user_id == user_id,
                UserSession.is_active == True
            )
        )
        result = await self.session.execute(stmt)
        sessions = result.scalars().all()
        
        count = 0
        for session in sessions:
            session.is_active = False
            session.logout_at = datetime.now(timezone.utc)
            count += 1
        
        await self.session.commit()
        return count

    async def cleanup_expired_sessions(self) -> int:
        """Remove sessões expiradas"""
        stmt = delete(UserSession).where(
            or_(
                UserSession.expires_at < datetime.now(timezone.utc),
                and_(
                    UserSession.is_active == False,
                    UserSession.logout_at < datetime.now(timezone.utc) - timedelta(days=7)
                )
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount

    async def get_user_active_sessions(self, user_id: int) -> List[UserSession]:
        """Busca sessões ativas de um usuário"""
        stmt = select(UserSession).where(
            and_(
                UserSession.user_id == user_id,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        ).order_by(UserSession.last_activity.desc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_session_stats(self) -> dict:
        """Busca estatísticas de sessões"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        active_stmt = select(func.count(UserSession.id)).where(
            and_(
                UserSession.is_active == True,
                UserSession.expires_at > now
            )
        )
        active_result = await self.session.execute(active_stmt)
        active_sessions = active_result.scalar()

        # Sessões criadas hoje
        today_stmt = select(func.count(UserSession.id)).where(
            UserSession.login_at >= today_start
        )
        today_result = await self.session.execute(today_stmt)
        total_sessions_today = today_result.scalar()

        # Usuários únicos que fizeram login hoje
        unique_users_stmt = select(func.count(func.distinct(UserSession.user_id))).where(
            UserSession.login_at >= today_start
        )
        unique_users_result = await self.session.execute(unique_users_stmt)
        unique_users_today = unique_users_result.scalar()

        # Duração média das sessões (em minutos)
        avg_duration_stmt = select(
            func.avg(
                func.extract('epoch', UserSession.last_activity - UserSession.login_at) / 60
            )
        ).where(
            and_(
                UserSession.logout_at.isnot(None),
                UserSession.login_at >= today_start
            )
        )
        avg_duration_result = await self.session.execute(avg_duration_stmt)
        avg_duration = avg_duration_result.scalar() or 0

        # Sessões por dispositivo (simplificado)
        device_stmt = select(
            func.coalesce(UserSession.device_info, 'Unknown'),
            func.count(UserSession.id)
        ).where(
            UserSession.login_at >= today_start
        ).group_by(UserSession.device_info)
        
        device_result = await self.session.execute(device_stmt)
        sessions_by_device = {device or 'Unknown': count for device, count in device_result.fetchall()}

        return {
            "active_sessions": active_sessions,
            "total_sessions_today": total_sessions_today,
            "unique_users_today": unique_users_today,
            "average_session_duration": round(avg_duration, 2),
            "sessions_by_device": sessions_by_device,
        }
