from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

class TransactionStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="booking.id", index=True)
    amount: Decimal
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    

class TransactionCreate(SQLModel):
    booking_id: int
    amount: Decimal
    status: TransactionStatus = TransactionStatus.PENDING


class TransactionUpdate(SQLModel):
    status: TransactionStatus    


class TransactionResponse(SQLModel):
    id: int
    booking_id: int
    amount: Decimal
    status: TransactionStatus
    created_at: datetime    
    model_config = {"from_attributes": True}