from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

class StatusBooking(str, Enum):
    RESERVED = 'reserved'
    CANCELED = 'canceled'
    CONFIRMED = 'confirmed'  


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    check_in: datetime
    check_out: datetime    
    user_id: int = Field(foreign_key="user.id", index=True)
    status: StatusBooking = Field(default=StatusBooking.RESERVED)  


class BookingCreate(SQLModel):     
    check_in: datetime
    check_out: datetime    
    user_id: int
    status: StatusBooking = StatusBooking.RESERVED


class BookingUpdate(SQLModel):    
    status: StatusBooking


class BookingResponse(SQLModel):
    id: int    
    check_in: datetime
    check_out: datetime    
    user_id: int
    status: StatusBooking
    model_config = {"from_attributes": True}