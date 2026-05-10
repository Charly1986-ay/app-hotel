from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import get_session


def get_db() -> Session:
    return next(get_session())


# db: Session = Depends(get_db)
DBSession = Annotated[Session, Depends(get_db)]
# db: DBSession