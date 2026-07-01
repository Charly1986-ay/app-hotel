from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import RoomNotFound
from app.models.room import Room, RoomCreate, RoomUpdate, StatusRoom
from app.repository.room_repository import RoomRepository

class RoomServices:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.room_repository = RoomRepository(db=db)


    async def get_status_room(self, status_room: str) -> list[Room]:  
        if status_room == 'all':
            return await self.room_repository.get_all() # Si está vacía, devuelve [] con paz mental.

        valid_types = [t.value for t in StatusRoom]
        if status_room not in valid_types:
            raise RoomNotFound() # O un HTTPException 400 por estado inválido

        enum_type = StatusRoom(status_room)
        rooms = await self.room_repository.get_by_status_room(status=enum_type)

        if not rooms:
            raise RoomNotFound()

        return rooms
    

    async def createRoom(self, room: RoomCreate) -> Room:
        # Desempaquetamos de forma dinámica. SQLModel se encarga del resto.
        room_db = Room(**room.model_dump())

        return await self.room_repository.create(room=room_db) 
    

    async def updateRoom(self, update: RoomUpdate, room_id: int) -> Room:
        # 1. Buscamos y modificamos mediante el repositorio
        room_db = await self.room_repository.get(room_id=room_id)
        if not room_db:
            raise RoomNotFound()
        
        room_dict = update.model_dump(exclude_unset=True)
        room = await self.room_repository.update(room=room_db, updates=room_dict)
        
        # 2. El servicio es el encargado de cerrar la transacción de esta operación única
        await self.room_repository.db.commit()
        await self.room_repository.db.refresh(room)
        
        return room       