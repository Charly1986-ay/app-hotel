from sqlmodel import col, select, Session

from app.models.booking import Booking, BookingCreate, BookingRoom

from datetime import date

from app.models.room import Room
from app.models.payment import Payment

class BookingRepository:
    def __init__(self, db: Session):
        self.db = db


    def get(self, booking_id: int) -> Booking | None:
        return self.db.get(Booking, booking_id)
    
    
    def get_check_in(self, check_in: date) -> list[Booking] | None:
        return self.db.exec(
            select(Booking).where(Booking.check_in == check_in)).all()
    

    def get_check_out(self, check_out: date) -> list[Booking] | None:
        return self.db.exec(
            select(Booking).where(Booking.check_out == check_out)).all()
    

    def get_all_available_rooms(self, start: date, end: date) -> list[Room]:
        """
        Busca todas las habitaciones disponibles.
        """
        
        # 1. Subconsulta: IDs de habitaciones con conflictos de fechas
        # Se une la tabla intermedia (BookingRoom) con la de reservas (Booking)
        rooms_with_conflict = (
            select(BookingRoom.room_id)
            .join(Booking)
            .where(
                Booking.check_in < end,
                Booking.check_out > start,
                # Booking.status != StatusBooking.CANCELLED (Sugerido: omitir canceladas)
            )
        )

        # 2. Consulta principal: Seleccionar habitaciones que NO estén en la subconsulta
        statement = (
            select(Room)
            .where(
                col(Room.id).not_in(rooms_with_conflict)
            )
            .where(Room.status == 'available')
        )

        # 3. Ejecución
        return self.db.exec(statement).all()
    

    def save_all(self, booking_obj: Booking, payment_obj: Payment) -> Booking:
        try:
            self.db.add(booking_obj)
            self.db.flush() # Esto genera el ID de la reserva sin cerrar la transacción
            
            payment_obj.booking_id = booking_obj.id # Asignamos el ID generado
            self.db.add(payment_obj)
            
            self.db.commit() # Guardamos ambos o nada
            self.db.refresh(booking_obj)
            return booking_obj
        except Exception as e:
            self.db.rollback() # Si algo falla, limpiamos la DB
            raise e
    

    def update(self, booking: Booking, updates: dict) -> Booking:        
        for key, value in updates.items():
            setattr(booking, key, value)

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking