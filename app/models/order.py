from datetime import date
from enum import Enum
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class StatusOrder(str, Enum):
    PENDING = 'pending'   
    APPROVED = 'approved'
    REFUSED = 'refused'
    CANCELED = 'canceled'


class Order(SQLModel, table=True):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}
    id: int = Field(default=None, primary_key=True)
    total: int = Field(default=0)    
    created_at: date = Field(
        default_factory = lambda: date.today(), 
        nullable = False
    )
    status: StatusOrder = Field(default=StatusOrder.PENDING)


class OrderCreate(SQLModel):
    total: int
    status: StatusOrder = StatusOrder.PENDING.value 

class OrderUpdate(SQLModel):    
    status: Optional[StatusOrder]

class OrderResponse(SQLModel):
    id: int
    total: int
    created_at: date
    status: StatusOrder
    model_config = ConfigDict(from_attributes=True)