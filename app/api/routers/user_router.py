from typing import Annotated

from fastapi import BackgroundTasks, Form, HTTPException, status, Request
from fastapi.routing import APIRouter
from app.core.exceptions import EmailExistsException
from app.core.jinja import templates
from app.dependencies.db_deps import DBSession
from app.models.user import Role, UserCreate, UserResponse
from app.services import user_services


router = APIRouter()

@router.get('', name='account_user')
def get_index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='register.html'        
    )


@router.post('/register', response_model=UserResponse)
def register_user(
    email: Annotated[str, Form()],
    full_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: DBSession,
    background_tasks: BackgroundTasks
):
    try:
        user = UserCreate(
            email=email,
            full_name=full_name,
            password=password,
            role=Role.CLIENT.value
        )

        return user_services.register(user=user, db=db, background_tasks=background_tasks)
    except EmailExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email ya existe en la base de datos'
        )