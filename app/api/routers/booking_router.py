from datetime import date

from fastapi import Request, status
from fastapi.routing import APIRouter
from app.dependencies.db_deps import DBSession
from app.core.jinja import templates
from app.models.room import RoomResponse
#from app.services import booking_services as services
from app.repository.booking_repository import BookingRepository


router = APIRouter()

@router.get('/', name='index', response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_index(request: Request, db: DBSession):    
    repo = BookingRepository(db=db)
    today = date.today()

    return templates.TemplateResponse(
        request=request, 
        name='index.html',
        context={"rooms": repo.get_all_available_rooms(
                start=today,
                end=today                
            )
        }
    )

@router.get('/payment', name='booking')
def get_payment_template(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='payment.html'        
    )


@router.post('/booking', response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: Request, db: DBSession):
    pass