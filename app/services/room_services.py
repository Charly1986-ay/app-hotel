from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import RoomNotFound
from app.models.room import Room, RoomCreate, RoomUpdate
from app.repository.room_repository import RoomRepository

class RoomServices:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.room_repository = RoomRepository(db=db)


    async def get_rooms_not_available(self) -> list[Room]:
        rooms = await self.room_repository.get_rooms_not_available()

        if not rooms:
            raise RoomNotFound()

        return rooms
    

    async def createRoom(self, room: RoomCreate) -> Room:
        # Desempaquetamos de forma dinámica. SQLModel se encarga del resto.
        room_db = Room(**room.model_dump())

        return await self.room_repository.create(room=room_db) 
    

    async def updateRoom(self, update: RoomUpdate, room_id: int) -> Room:
        room_db = await self.room_repository.get(room_id=room_id)

        if not room_db:
            raise RoomNotFound()
        
        room_dict = update.model_dump(exclude_unset=True)

        return await self.room_repository.update(
            room=room_db, 
            updates=room_dict
        )       