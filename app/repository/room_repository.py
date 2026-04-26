from sqlmodel import select, Session

from app.models.room import Room, TypeRoom

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db


    def get(self, room_id: int) -> Room | None:
        return self.db.get(Room, room_id)
    
    
    def get_by_type_room(self, room_type: TypeRoom) -> Room | None:
        return self.db.exec(
            select(Room).where(Room.type_room == room_type)).all()
    

    def get_by_status_room(self, status_room: TypeRoom) -> Room | None:
        return self.db.exec(
            select(Room).where(Room.status == status_room)).all()
    

    def create(self, room: Room) -> Room:
        self.db.add(room)
        # self.db.flush()
        self.db.commit()
        self.db.refresh(room)
        return room
    

    def update(self, room: Room, updates: dict) -> Room:        
        for key, value in updates.items():
            setattr(room, key, value)

        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room