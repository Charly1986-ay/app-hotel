from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.user import User

class PaymentStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class TypeCurrency(str, Enum):
    USD = 'usd'
    EUR = 'eur'
    AR = 'ar'


class Payment(SQLModel, table=True):
    __tablename__ = 'payment'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)    
    user_id: int = Field(foreign_key='user.id', index=True)
    booking_id: Optional[int] = Field(default=None, foreign_key='booking.id', index=True)  
    # Dinero (En centavos) 
    amount: int = Field(default=0)   
    currency: str = Field(default=TypeCurrency.USD.value)       
    stripe_payment_intent_id: str = Field(unique=True, index=True)
    #stripe_client_secret: Optional[str] = None  
    status: str = Field(default=PaymentStatus.PENDING.value)  
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relaciones para navegar los objetos
    user: Optional["User"] = Relationship(back_populates="payments")
    booking: Optional["Booking"] = Relationship(back_populates="payment")


class PaymentCreate(SQLModel):
    user_id: int
    booking_id: int
    amount: int   
    currency: str = TypeCurrency.USD 
    stripe_payment_intent_id: str
    status: str = PaymentStatus.PENDING


class PaymentResponse(SQLModel):
    id: int
    user_id: int
    booking_id: int
    amount: int
    currency: str
    status: str
    created_at: datetime    
    model_config = {'from_attributes': True}