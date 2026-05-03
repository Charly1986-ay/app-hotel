from sqlmodel import Session

from app.models.room import RoomUpdate, StatusRoom
from app.repository.room_repository import RoomRepository
from app.repository.booking_repository import BookingRepository

from datetime import date


def check_out(db: Session, check_out: date) -> None:    
    try:
        repoBooking = BookingRepository(db=db)
        bookings = repoBooking.get_check_out(check_out=check_out)
        if bookings:
            repoRoom = RoomRepository(db=db)
            for booking in bookings:
                for room in booking.rooms:
                    if room.status == StatusRoom.OCCUPIED:
                        roomUpdate = RoomUpdate(status=StatusRoom.PENDING_CLEANING)
                        repoRoom.update(room=room, updates=roomUpdate.model_dump(exclude_unset=True))
                        print(f'Habitación {room.id} enviada a limpieza.')
            db.commit()
        else:
            print('no hay reservas')
    except Exception as e:
        print(f"Error en el job OUT: {e}")
        db.rollback()    


def check_in(db: Session, check_in: date):
    try:
        repoBooking = BookingRepository(db=db)
        bookings = repoBooking.get_check_in(check_in=check_in)
        if bookings:
            repoRoom = RoomRepository(db=db)
            for booking in bookings:
                for room in booking.rooms:
                    if room.status == StatusRoom.AVAILABLE:
                        roomUpdate = RoomUpdate(status=StatusRoom.OCCUPIED)
                        repoRoom.update(room=room, updates=roomUpdate.model_dump(exclude_unset=True))
                        print(f"Habitación {room.id} bloqueada por Check-in.")
            db.commit()
        else:
            print('no hay reservas')
    except Exception as e:
        print(f"Error en el job IN: {e}")
        db.rollback()