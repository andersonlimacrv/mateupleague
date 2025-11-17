from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass
from sqlalchemy.engine import make_url
from typing import AsyncGenerator
import asyncio

from app.core.config import settings


class Base(MappedAsDataclass, DeclarativeBase):...

db_url = make_url(settings.DATABASE_URL)

async_engine = create_async_engine(
    db_url,
    echo=True,
    echo_pool=False,
    pool_size=10,  # Tamanho do pool de conexões
    max_overflow=20,  # Conexões adicionais além do pool_size
    pool_timeout=30,  # Tempo de espera por uma conexão do pool (em segundos)
    pool_recycle=1800,  # Tempo para reciclar uma conexão (em segundos)
    pool_pre_ping=True,  # Habilita ping antes de usar a conexão do pool
)

local_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)

async def async_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = local_session
    async with async_session() as db_session:
        yield db_session


# Função para criar todas as tabelas
async def create_all_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        from app.models.user import User
        

        await conn.run_sync(Base.metadata.create_all)


# Função principal para rodar a criação das tabelas
async def main():
    await create_all_tables(async_engine)


if __name__ == "__main__":
    asyncio.run(main())