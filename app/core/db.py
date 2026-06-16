from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

import app.models

# 1. Creamos el motor asíncrono (create_async_engine)
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 2. Creamos el generador de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def init_db() -> None:    
    # Nota: create_all es sincrónico por naturaleza, así que para ejecutarlo 
    # en un entorno asíncrono necesitamos usar 'run_sync'
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# 3. La dependencia cambia a AsyncIterator y retorna una AsyncSession
async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session