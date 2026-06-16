from datetime import date
# Cambiamos a AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.room import RoomUpdate, StatusRoom
from app.repository.room_repository import RoomRepository
from app.repository.booking_repository import BookingRepository


# 1. Convertimos la función a asíncrona y tipamos con AsyncSession
async def check_out(db: AsyncSession, check_out: date) -> None:    
    try:
        repoBooking = BookingRepository(db=db)
        
        # 2. Agregamos await (asumiendo que tus repositorios serán asíncronos)
        bookings = await repoBooking.get_check_out(check_out=check_out)
        
        if bookings:
            repoRoom = RoomRepository(db=db)
            for booking in bookings:
                for room in booking.rooms:
                    if room.status == StatusRoom.OCCUPIED:
                        roomUpdate = RoomUpdate(status=StatusRoom.PENDING_CLEANING)
                        
                        # 3. Agregamos await en la actualización
                        await repoRoom.update(room=room, updates=roomUpdate.model_dump(exclude_unset=True))
                        print(f'Habitación {room.id} enviada a limpieza.')
            
            # 4. El commit ahora es asíncrono
            await db.commit()
        else:
            print('no hay reservas')
    except Exception as e:
        print(f"Error en el job OUT: {e}")
        # 5. El rollback también es asíncrono
        await db.rollback()    


# 1. Convertimos a asíncrona y tipamos con AsyncSession
async def check_in(db: AsyncSession, check_in: date) -> None:
    try:
        repoBooking = BookingRepository(db=db)
        
        # 2. Agregamos await
        bookings = await repoBooking.get_check_in(check_in=check_in)
        
        if bookings:
            repoRoom = RoomRepository(db=db)
            for booking in bookings:
                for room in booking.rooms:
                    if room.status == StatusRoom.AVAILABLE:
                        roomUpdate = RoomUpdate(status=StatusRoom.OCCUPIED)
                        
                        # 3. Agregamos await
                        await repoRoom.update(room=room, updates=roomUpdate.model_dump(exclude_unset=True))
                        print(f"Habitación {room.id} bloqueada por Check-in.")
            
            # 4. El commit ahora es asíncrono
            await db.commit()
        else:
            print('no hay reservas')
    except Exception as e:
        print(f"Error en el job IN: {e}")
        # 5. El rollback también es asíncrono
        await db.rollback()