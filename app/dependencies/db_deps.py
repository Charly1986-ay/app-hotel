from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession # <-- Importación nativa de SQLModel

from app.core.db import get_session


DBSession = Annotated[AsyncSession, Depends(get_session)]