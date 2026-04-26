from datetime import date
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.room import Room

class StatusBooking(str, Enum):
    CANCELED = 'canceled'
    CONFIRMED = 'confirmed'  


class BookingRoom(SQLModel, table=True):
    booking_id: int = Field(foreign_key="booking.id", primary_key=True)
    room_id: int = Field(foreign_key="room.id", primary_key=True)


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    check_in: date   # fecha ingreso
    check_out: date  # fecha de salida    
    user_id: int = Field(foreign_key="user.id", index=True)
    status: StatusBooking = Field(default=StatusBooking.CONFIRMED)  
    rooms: List["Room"] = Relationship(back_populates="bookings", link_model=BookingRoom)


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