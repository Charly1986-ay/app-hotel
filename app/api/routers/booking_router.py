from datetime import date

from fastapi import Request, status
from fastapi.routing import APIRouter
from app.dependencies.db_deps import DBSession
from app.core.jinja import templates
from app.models.room import RoomResponse
from app.repository.booking_repository import BookingRepository


router = APIRouter()

@router.get('/', name='index', response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_index(request: Request, db: DBSession):
    booking_repository = BookingRepository(db=db)
    today = date.today()

    return templates.TemplateResponse(
        request=request, 
        name='index.html',
        context={"rooms": booking_repository.get_all_available_rooms(
                start=today,
                end=today  
            )
        }
    )

@router.post('/reserve', response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: Request, db: DBSession):
    pass