from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Role(str, Enum):
    GUEST = 'guest'               # Cliente/huésped
    RECEPTIONIST = 'receptionist' # Recepcionista
    SUPERVISOR = 'supervisor'     # Supervisor de limpieza/operaciones
    MANAGER = 'manager'           # Gerente


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    role: Role = Field(default=Role.GUEST)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class UserCreate(SQLModel):
    email: str
    full_name: str
    password: str
    role: Role = Role.GUEST
    status: UserStatus = UserStatus.ACTIVE


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None   


class Login(SQLModel):
    email: str    
    password: str
    

class UserResponse(SQLModel):
    id: int
    email: str
    full_name: str
    model_config = {"from_attributes": True}