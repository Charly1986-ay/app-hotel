from fastapi import APIRouter, Depends, Request
from app.core.jinja import templates
from app.dependencies.db_deps import DBSession
from app.models.room import RoomResponse, RoomUpdate
from app.models.user import User
from app.dependencies.permission import supervisor_dependency
from app.services.room_services import RoomServices
from app.services.manager_websocket import manager_rooms

router = APIRouter()

@router.get('', name='module_supervisor')
def get_supervisor(
    request: Request, 
    current_user: User = supervisor_dependency
):  
    return templates.TemplateResponse(
        request=request, 
        name='panel/supervisor.html',
        context={"user": current_user} # ◄ Le pasamos el usuario a Jinja por si quieres usarlo en el HTML
    )


# FACETA 1: Actualizar solo el estado (Limpieza, Recepción, etc.)
@router.patch("/{room_id}/status", response_model=RoomResponse)
async def update_room_status(
    room_id: int, 
    payload: RoomUpdate, 
    db: DBSession,
    current_user = supervisor_dependency
):
    room_service = RoomServices(db=db)
    updated_room = await room_service.updateRoom(update=payload, room_id=room_id)
    
    response_data = RoomResponse.model_validate(updated_room)
    
    # Evento específico para cambios de estado rápido
    await manager_rooms.broadcast(
        event_name="room_status_updated",
        data=response_data
    )
    
    return response_data


# FACETA 2: Actualizar la información general de la habitación (Administración)
@router.patch("/{room_id}", response_model=RoomResponse)
async def update_room_details(
    room_id: int, 
    payload: RoomUpdate, 
    db: DBSession,
    current_user = supervisor_dependency
):
    room_service = RoomServices(db=db)
    updated_room = await room_service.updateRoom(update=payload, room_id=room_id)
    
    response_data = RoomResponse.model_validate(updated_room)
    
    # Evento general para edición estructural de la habitación
    await manager_rooms.broadcast(
        event_name="room_details_updated",
        data=response_data
    )
    
    return response_data