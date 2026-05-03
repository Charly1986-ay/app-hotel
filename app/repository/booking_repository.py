from sqlmodel import col, select, Session

from app.models.booking import Booking, BookingRoom

from datetime import date

from app.models.room import Room

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
    

    def get_available_rooms_by_type(self, room_type: str, start: date, end: date) -> list[Room]:
        """
        Busca habitaciones disponibles considerando la relación Many-to-Many.
        Filtra por tipo y excluye las que tienen conflictos en Booking.
        """
        
        # 1. Subconsulta: Buscamos los IDs de las habitaciones que están ocupadas.
        # Necesitamos unir BookingRoom con Booking para filtrar por fechas.
        rooms_with_conflict = (
            select(BookingRoom.room_id)
            .join(Booking)  # Unimos la tabla intermedia con la de reservas
            .where(
                Booking.check_in < end,
                Booking.check_out > start,
                # Opcional: Solo considerar reservas confirmadas o pagadas
                # Booking.status == StatusBooking.CONFIRMED 
            )
        )

        # 2. Consulta principal: Habitaciones de un tipo que no estén en la subconsulta
        statement = (
            select(Room)
            .where(
                Room.type_room == room_type,
                col(Room.id).not_in(rooms_with_conflict)
            )
        )

        # 3. Ejecución y retorno de la lista de objetos Room
        return self.db.exec(statement).all()
    

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.flush()
        #self.db.commit()
        self.db.refresh(booking)
        return booking
    

    def update(self, booking: Booking, updates: dict) -> Booking:        
        for key, value in updates.items():
            setattr(booking, key, value)

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking