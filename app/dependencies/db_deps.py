from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession # <-- Importación nativa de SQLModel

from app.core.db import get_session

# La función ahora es asíncrona para poder resolver el generador de la DB
async def get_db() -> AsyncSession:
    # Usamos anext con await porque get_session() ahora es un generador asíncrono
    return await anext(get_session())

# Tu anotación limpia usando la sesión asíncrona de SQLModel
DBSession = Annotated[AsyncSession, Depends(get_db)]