from datetime import date
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.transaction import Transaction

class StatusBooking(str, Enum):
    CANCELED = 'canceled'
    CONFIRMED = 'confirmed'  


class BookingRoom(SQLModel, table=True):
    __tablename__ = "bookingroom" # Nombre explícito
    __table_args__ = {"extend_existing": True}
    booking_id: int = Field(foreign_key="booking.id", primary_key=True)
    room_id: int = Field(foreign_key="room.id", primary_key=True)


class Booking(SQLModel, table=True):
    __tablename__ = "booking" # Nombre explícito
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)    
    check_in: date   # fecha ingreso
    check_out: date  # fecha de salida    
    user_id: int = Field(foreign_key="user.id", index=True)
    status: StatusBooking = Field(default=StatusBooking.CONFIRMED)  
    
    rooms: List["Room"] = Relationship(back_populates="bookings", link_model=BookingRoom)
    # Relación 1:1: Usamos string "Transaction"
    transaction: Optional["Transaction"] = Relationship(back_populates="booking")

class BookingCreate(SQLModel):     
    check_in: date
    check_out: date  
    user_id: int
    status: StatusBooking = StatusBooking.CONFIRMED


class BookingUpdate(SQLModel):    
    status: StatusBooking


class BookingResponse(SQLModel):
    id: int    
    check_in: date
    check_out: date   
    user_id: int
    status: StatusBooking
    model_config = {"from_attributes": True}