from sqlmodel import col, select
# 1. Conexión asíncrona dedicada
from sqlmodel.ext.asyncio.session import AsyncSession

# Importamos los Enums correctos desde tus modelos
from app.models.room import Room, TypeRoom, StatusRoom


class RoomRepository:
    # 2. El constructor recibe la sesión asíncrona
    def __init__(self, db: AsyncSession):
        self.db = db

    # 3. Todos los métodos con 'async def' y sus respectivos 'await'
    async def get(self, room_id: int) -> Room | None:
        return await self.db.get(Room, room_id)
    
    async def get_all(self) -> list[Room]:
        result = await self.db.exec(select(Room))
        return result.all()
    
    async def get_by_ids(self, ids: list[int]) -> list[Room]:
        statement = select(Room).where(col(Room.id).in_(ids))        
        result = await self.db.exec(statement)
        return result.all()
    
    async def get_by_type_room(self, room_type: TypeRoom) -> list[Room]:
        result = await self.db.exec(
            select(Room).where(Room.type_room == room_type)
        )
        return result.all()

    # CORREGIDO: Ahora usa 'status: StatusRoom' y el retorno indica la lista correctamente
    async def get_by_status_room(self, status: StatusRoom) -> list[Room]:
        result = await self.db.exec(
            select(Room).where(Room.status == status)
        )
        return result.all()

    async def create(self, room: Room) -> Room:
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room

    async def update(self, room: Room, updates: dict) -> Room:        
        for key, value in updates.items():
            setattr(room, key, value)

        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        return room