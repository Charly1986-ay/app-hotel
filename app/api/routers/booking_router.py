from datetime import date
from typing import Annotated

from fastapi import Body, Form, HTTPException, Request, status
from fastapi.routing import APIRouter
from app.core.exceptions import PaymentException, RoomNotFound
from app.dependencies.db_deps import DBSession
from app.dependencies.permission import user_dependency
from app.core.jinja import templates
from app.core.config import settings
from app.models.booking import BookingCreate, BookingResponse
from app.models.payment import PaymentCreate
from app.models.room import RoomResponse
from app.models.user import User
from app.services.booking_services import BookingServices


router = APIRouter()

@router.get('/', name='index', response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_index(request: Request, db: DBSession):    
    services = BookingServices(db=db)
    today = date.today()

    return templates.TemplateResponse(
        request=request, 
        name='index.html',
        context={'rooms': services.get_all_available_rooms_services(
                start=today,
                end=today                
            )
        }
    )

@router.get('/payment', name='payment')
def get_payment_template(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='payment.html'        
    )


@router.post('/payment', response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    db: DBSession,
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
        return services.create_reservation(
            booking=booking_model, 
            type_card='card', 
            token_id=token, 
            currency='usd'
        )
    except RoomNotFound:
        raise HTTPException(status_code=404, detail='No hay habitaciones para procesar')
    except PaymentException:
        raise HTTPException(status_code=402, detail='No se ha podido realizar el pago')