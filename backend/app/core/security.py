from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jwt import DecodeError, ExpiredSignatureError, decode, encode
import bcrypt

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from app.core.database.db import async_get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from sqlalchemy import select

from app.schemas.token import TokenData
from app.core.config import settings
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
Token = Annotated[str, Depends(oauth2_scheme)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "name": ""})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY_HASH, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "name": ""})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY_HASH_REFRESH, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def check_refresh_token(token: Token, db: db_session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY_HASH_REFRESH, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await db.scalar(select(User).where(User.username == token_data.username))

    if user is None:
        raise credentials_exception

    return user


def get_password_hash(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


async def get_current_user(token: Token, db: db_session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY_HASH, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
        token_data = TokenData(username=user_id)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await db.scalar(select(User).where(User.username == token_data.username))

    if user is None:
        raise credentials_exception

    return user

async def get_current_user_ws(token: str, db: db_session):
    try: 
        payload = decode(
            token, settings.SECRET_KEY_HASH, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: não foi encontrado o 'sub' no payload"
            )
        token_data = TokenData(username=user_id)

    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao decodificar o token: Token inválido"
        )
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )

    user = await db.scalar(select(User).where(User.username == token_data.username))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return user

