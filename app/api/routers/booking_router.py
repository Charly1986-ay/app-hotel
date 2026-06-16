from datetime import date
from typing import List

from fastapi import BackgroundTasks, Body, HTTPException, Query, Request, status
from fastapi.routing import APIRouter

from app.core.exceptions import PaymentException, RoomNotFound
from app.dependencies.db_deps import DBSession
from app.dependencies.permission import user_dependency
from app.core.jinja import templates
from app.models.booking import BookingCreate, BookingResponse
from app.models.room import RoomResponse
from app.models.user import User
from app.services.booking_services import BookingServices


router = APIRouter()

@router.get('/', name='index')
def get_index(request: Request):  
    # Leer archivos del disco local con Jinja sigue siendo perfecto de forma sincrónica
    return templates.TemplateResponse(
        request=request, 
        name='index.html'
    )


@router.get(
        '/api/rooms', 
        name='room_avalible', 
        response_model=List[RoomResponse], 
        status_code=status.HTTP_200_OK
)
# CORRECCIÓN: Convertimos a 'async def' porque el servicio interno consulta la DB de forma asíncrona
async def get_rooms_availible(
    request: Request, 
    db: DBSession, 
    start: date = Query(..., alias="checkin"), 
    end: date = Query(..., alias="checkout")
):
    services = BookingServices(db=db)   

    # CORRECCIÓN: Agregamos el 'await' obligatorio para esperar la lista de habitaciones disponibles
    return await services.get_all_available_rooms_services(
        start=start,
        end=end
    )
        
    

@router.get('/api/payment', name='payment')
def get_payment_template(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='payment.html'        
    )


@router.post('/api/payment', response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
# CORRECCIÓN: Convertimos a 'async def' debido a que involucra pasarela de pago (Stripe) y escrituras en DB
async def create_booking(
    db: DBSession,
    background_tasks: BackgroundTasks,   
    token: str = Body(...),      
    booking: dict = Body(...),       
    user: User = user_dependency       
):
    booking_model = BookingCreate(
        check_in=booking['check_in'],
        check_out=booking['check_out'],
        user_id=user.id,
        room_ids=booking['room_ids'] 
    )
    
    services = BookingServices(db=db)

    try:
        # CORRECCIÓN: Agregamos el 'await' fundamental para orquestar toda la transacción asíncrona
        return await services.create_reservation(
            booking=booking_model, 
            type_card='card', 
            token_id=token, 
            currency='usd',
            user=user,                                          
            background_tasks=background_tasks   
        )
    except RoomNotFound:
        raise HTTPException(status_code=404, detail='No hay habitaciones para procesar')
    except PaymentException:
        raise HTTPException(status_code=402, detail='No se ha podido realizar el pago')