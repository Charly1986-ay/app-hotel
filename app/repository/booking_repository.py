from datetime import date
from sqlmodel import col, select
# 1. Cambiamos el tipo de sesión al módulo de extensión asíncrona de SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.booking import Booking, BookingCreate, BookingRoom
from app.models.payment import Payment
from app.models.room import Room


class BookingRepository:   
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get(self, booking_id: int) -> Booking | None:
        return await self.db.get(Booking, booking_id)
    
    async def get_check_in(self, check_in: date) -> list[Booking] | None:
        result = await self.db.exec(
            select(Booking).where(Booking.check_in == check_in)
        )
        return result.all()

    async def get_check_out(self, check_out: date) -> list[Booking] | None:
        result = await self.db.exec(
            select(Booking).where(Booking.check_out == check_out)
        )
        return result.all()

    async def get_all_available_rooms(self, start: date, end: date) -> list[Room]:
        """
        Busca todas las habitaciones disponibles de manera asíncrona.
        """
        # 1. Subconsulta: IDs de habitaciones con conflictos de fechas
        rooms_with_conflict = (
            select(BookingRoom.room_id)
            .join(Booking)
            .where(
                Booking.check_in < end,
                Booking.check_out > start,
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

        # 3. Ejecución asíncrona
        result = await self.db.exec(statement)
        return result.all()

    async def save_all(self, booking_obj: Booking, payment_obj: Payment) -> Booking:
        try:
            self.db.add(booking_obj)
            # El flush ahora requiere 'await' para hablar con SQLite de forma asíncrona
            await self.db.flush() 
            
            payment_obj.booking_id = booking_obj.id 
            self.db.add(payment_obj)
            
            # Operaciones de guardado asíncronas
            await self.db.commit() 
            await self.db.refresh(booking_obj)
            return booking_obj
        except Exception as e:
            await self.db.rollback() 
            raise e

    async def update(self, booking: Booking, updates: dict) -> Booking:        
        for key, value in updates.items():
            setattr(booking, key, value)

        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking