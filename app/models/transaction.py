from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.booking import Booking

class TransactionStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="booking.id", unique=True)
    amount: Decimal
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relación: Usamos string "Booking"
    booking: Optional["Booking"] = Relationship(back_populates="transaction")

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