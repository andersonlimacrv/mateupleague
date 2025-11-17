from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.schemas.token import Token, RefreshToken, RefreshTokenData
from app.models.user import User
from app.repositories.users import UserRepository
from app.repositories.user_sessions import UserSessionRepository
from app.services.user_sessions import UserSessionService

router = APIRouter()

db_session = Annotated[AsyncSession, Depends(async_get_db_session)]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
current_user = Annotated[User, Depends(get_current_user)]
refreshToken = Annotated[RefreshTokenData, Depends()]


@router.post("/login", response_model=RefreshToken)
async def login_for_access_token(
    form_data: FormData, 
    db: db_session,
    request: Request
):
    user_repo = UserRepository(db)
    session_repo = UserSessionRepository(db)
    session_service = UserSessionService(session_repo)
    
    user = await user_repo.get_user_by_username(username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This username does not exist.",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )

    await user_repo.update_last_login(user)

    user_agent = request.headers.get("user-agent", "")
    ip_address = request.client.host if request.client else None
    
    session = await session_service.create_session(
        user=user,
        device_info=user_agent, 
        ip_address=ip_address,
        user_agent=user_agent
    )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.id})
    response = RefreshToken(
        access_token=access_token, 
        token_type="Bearer", 
        refresh_token=refresh_token
    )

    return response


@router.post("/refresh_token", response_model=RefreshToken)
async def refresh_acess_token(refresh_token_data: refreshToken, user: current_user):
    """WIP - está aceitando qualquer refresh token, futuramente irá ser salvo para comparar."""


@router.post("/logout")
async def logout(db: db_session, user: current_user):
    """Faz logout do usuário atual"""
    session_repo = UserSessionRepository(db)
    session_service = UserSessionService(session_repo)
    
    try:
        # Encerra todas as sessões do usuário
        count = await session_service.logout_all_user_sessions(user.id)
        return {"message": f"Logged out successfully. {count} sessions ended."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {e}"
        )
