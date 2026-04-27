from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

import app.models.booking as booking_mod

# 2. Importamos solo para el editor de código
if TYPE_CHECKING:
    from app.models.booking import Booking

class TypeRoom(str, Enum):
    STANDARD = 'standard'
    EXECUTIVE = 'executive'
    SUITE = 'suite'    

class StatusRoom(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    PENDING_CLEANING = "pending_cleaning"
    MAINTENANCE = "maintenance"  


class Room(SQLModel, table=True):
    __tablename__ = "room"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    # ge → mínimo permitido (inclusive), le → máximo permitido (inclusive)
    bed_count: int = Field(default=1, ge=1, le=3) # cantidad de camas
    max_capacity: int = Field(default=1, ge=1, le=4) # capacidad maxima
    price: float
    type_room: TypeRoom = Field(default=TypeRoom.STANDARD)
    status: StatusRoom = Field(default=StatusRoom.AVAILABLE)
    
    # Relación muchos a muchos
    bookings: List["Booking"] = Relationship(
        back_populates="rooms", 
        link_model=booking_mod.BookingRoom
    )


class RoomCreate(SQLModel):
    bed_count: int
    max_capacity: int
    price: float
    type_room: TypeRoom = TypeRoom.STANDARD
    status: StatusRoom = StatusRoom.AVAILABLE


class RoomUpdate(SQLModel):
    bed_count: Optional[int]
    max_capacity: Optional[int]
    price: Optional[float]
    type_room: Optional[TypeRoom]
    status: Optional[StatusRoom]


class RoomResponse(SQLModel):
    id: int
    bed_count: int
    max_capacity: int
    price: float
    type_room: TypeRoom
    status: StatusRoom
    model_config = {"from_attributes": True}