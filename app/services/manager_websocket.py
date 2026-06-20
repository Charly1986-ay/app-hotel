from typing import Generic, TypeVar
from fastapi import WebSocket
from pydantic import BaseModel

from app.models.order import OrderResponse
from app.models.room import RoomResponse

T = TypeVar("T", bound=BaseModel)

class ConnectionManager(Generic[T]):
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, event_name: str, data: T):
        """
        Envía una notificación estructurada a todos los clientes.
        """
        message = {
            "event": event_name,
            "data": data.model_dump()
        }
        for connection in self.active_connections:
            await connection.send_json(message)

manager_rooms = ConnectionManager[RoomResponse]()
manager_orders = ConnectionManager[OrderResponse]()