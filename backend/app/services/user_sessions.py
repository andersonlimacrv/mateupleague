from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import hashlib

from app.models.user import User
from app.models.user_session import UserSession
from app.repositories.user_sessions import UserSessionRepository
from app.core.config import settings


class UserSessionService:
    def __init__(self, session_repository: UserSessionRepository):
        self.session_repository = session_repository

    def _generate_session_token(self) -> str:
        """Gera um token de sessão único"""
        return secrets.token_urlsafe(32)

    def _generate_refresh_token(self) -> str:
        """Gera um refresh token único"""
        return secrets.token_urlsafe(32)

    def _calculate_expires_at(self) -> datetime:
        """Calcula quando a sessão expira"""
        return datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    async def create_session(
        self,
        user: User,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserSession:
        """Cria uma nova sessão para o usuário"""
        try:
            # Encerra sessões antigas do mesmo usuário (opcional)
            # await self.session_repository.logout_all_user_sessions(user.id)
            
            session_data = {
                "user_id": user.id,
                "session_token": self._generate_session_token(),
                "refresh_token": self._generate_refresh_token(),
                "device_info": device_info,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "expires_at": self._calculate_expires_at(),
            }
            
            return await self.session_repository.create_session(session_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating session: {e}"
            )

    async def validate_session(self, session_token: str) -> Optional[UserSession]:
        """Valida uma sessão e retorna os dados se válida"""
        try:
            session = await self.session_repository.get_session_by_token(session_token)
            if session:
                # Atualiza última atividade
                await self.session_repository.update_session_activity(session.id)
            return session
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error validating session: {e}"
            )

    async def refresh_session(self, refresh_token: str) -> Optional[UserSession]:
        """Renova uma sessão usando o refresh token"""
        try:
            session = await self.session_repository.get_session_by_refresh_token(refresh_token)
            if session:
                # Gera novos tokens
                session.session_token = self._generate_session_token()
                session.refresh_token = self._generate_refresh_token()
                session.expires_at = self._calculate_expires_at()
                session.last_activity = datetime.now(timezone.utc)
                
                await self.session_repository.session.commit()
                await self.session_repository.session.refresh(session)
                
                return session
            return None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error refreshing session: {e}"
            )

    async def logout_session(self, session_token: str) -> bool:
        """Faz logout de uma sessão específica"""
        try:
            return await self.session_repository.logout_session(session_token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error logging out session: {e}"
            )

    async def logout_all_user_sessions(self, user_id: int) -> int:
        """Faz logout de todas as sessões de um usuário"""
        try:
            return await self.session_repository.logout_all_user_sessions(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error logging out all sessions: {e}"
            )

    async def get_user_sessions(self, user_id: int) -> list[UserSession]:
        """Busca todas as sessões ativas de um usuário"""
        try:
            return await self.session_repository.get_user_active_sessions(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting user sessions: {e}"
            )

    async def get_session_stats(self) -> dict:
        """Busca estatísticas de sessões"""
        try:
            return await self.session_repository.get_session_stats()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting session stats: {e}"
            )

    async def cleanup_expired_sessions(self) -> int:
        """Remove sessões expiradas"""
        try:
            return await self.session_repository.cleanup_expired_sessions()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error cleaning up sessions: {e}"
            )
