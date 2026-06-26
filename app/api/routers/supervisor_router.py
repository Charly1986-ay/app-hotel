from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status, Request
from app.core.exceptions import RoomNotFound
from app.core.jinja import templates
from app.dependencies.db_deps import DBSession
from app.models.room import RoomListNotAvailable, RoomResponse, RoomUpdate, StatusRoom, TypeRoom
from app.models.user import User
from app.dependencies.permission import supervisor_dependency
from app.services.room_services import RoomServices


router = APIRouter()

@router.get('', name='module_supervisor')
def get_supervisor(
    request: Request, 
    current_user: User = supervisor_dependency
):  
    return templates.TemplateResponse(
        request=request, 
        name='panel/supervisor.html',
        context={"user": current_user}
    )


# FACETA 1: Actualizar solo el estado (Limpieza, Recepción, etc.)
async def _change_room_status(room_id: int, status: StatusRoom, db: DBSession) -> RoomResponse:
    room_service = RoomServices(db=db)

    payload = RoomUpdate(status=status.value)
    updated_room = await room_service.updateRoom(update=payload, room_id=room_id)
    
    response_data = RoomResponse.model_validate(updated_room)
    
    return response_data


# --- ENDPOINTS PÚBLICOS ---

@router.patch("/rooms/{room_id}/available", response_model=RoomResponse)
async def set_available_status(
    room_id: int, 
    db: DBSession, 
    current_user = supervisor_dependency
):
    """Cambia el estado de una habitación a DISPONIBLE."""
    return await _change_room_status(room_id, StatusRoom.AVAILABLE, db)


@router.patch("/rooms/{room_id}/maintenance", response_model=RoomResponse)
async def set_maintenance_status(
    room_id: int, 
    db: DBSession, 
    current_user = supervisor_dependency
):
    """Cambia el estado de una habitación a MANTENIMIENTO."""
    return await _change_room_status(room_id, StatusRoom.MAINTENANCE, db)


# FACETA 2: Actualizar la información general de la habitación (Administración)
@router.patch("/rooms/{room_id}", response_model=RoomResponse)
async def update_room_details(
    room_id: int,     
    db: DBSession,
    bed_count: Annotated[int, Form()],
    max_capacity: Annotated[int, Form()],
    price: Annotated[int, Form()],
    type_room: Annotated[str, Form()],    
    current_user = supervisor_dependency
):
    # 1. Validamos el Enum (puede lanzar AttributeError)
    try:
        type_ = getattr(TypeRoom, type_room)
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de habitación '{type_room}' no es válido."
        )

    # 2. Armamos el payload de forma segura fuera del try
    payload = RoomUpdate(
        bed_count=bed_count,
        max_capacity=max_capacity,
        price=price,
        type_room=type_,        
    )
    
    room_service = RoomServices(db=db)
    
    # 3. Ejecutamos la consulta (puede lanzar RoomNotFound)
    try:
        updated_room = await room_service.updateRoom(update=payload, room_id=room_id)
    except RoomNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Habitación no encontrada'
        )
        
    # 4. Validamos y retornamos la respuesta
    response_data = RoomResponse.model_validate(updated_room)
    return response_data


@router.get("/rooms/not-available", response_model=RoomListNotAvailable)
async def get_rooms_not_available(
    request: Request,
    db: DBSession,     
    current_user = supervisor_dependency
):   
    
    try:
        room_services = RoomServices(db=db)
        rooms_db = await room_services.get_rooms_not_available()

        return {
            'rooms_not_available': rooms_db
        }        
            
    except RoomNotFound:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )