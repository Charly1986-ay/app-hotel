from typing import Annotated

from fastapi import Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from app.core.jinja import templates

from app.dependencies.db_deps import DBSession
from app.models.user import TokenResponse, User, UserLogin
from app.services import auth_services as services

from app.core.exceptions import UserNotFound, CredentialsException
from app.dependencies.permission import get_current_user_active

router = APIRouter()

@router.get('/login', name='login_user', response_class=HTMLResponse)
def login_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request, 
        name='login.html'        
    )

@router.post('/login', name='token_user', status_code=status.HTTP_200_OK)
def login(    
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response, 
    db: DBSession
) -> TokenResponse:
    try:
        login_data = UserLogin(email=email, password=password)
        token_data = services.login_services(user=login_data, db=db)
        
        response.set_cookie(
            key='access_token',
            value=token_data.access_token,
            httponly=True,
            secure=False, #=> True solo para produccion
            samesite='lax'
        )
        return token_data     
    
    except (UserNotFound, CredentialsException):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Usuario o contraseña incorrectos'
        )    


@router.get('/me', status_code=status.HTTP_200_OK)
def verify_user(user: User = Depends(get_current_user_active)):
    '''
        Endpoint universal de control de sesión.
        Si la cookie es válida y el usuario existe en la DB, devuelve 200 OK.
        Si la cookie no existe o venció, 'get_current_user_active' lanza 
        CredentialsException (401) automáticamente antes de entrar aquí.
    '''
    return {
        'authenticated': True,
        'id': user.id,
        'role': user.role  # Enviarlo te servirá en el frontend más adelante
    }