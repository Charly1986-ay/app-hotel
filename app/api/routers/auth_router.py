from tkinter import S
from typing import Annotated

from fastapi import Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from sqlmodel import Session
from app.core.jinja import templates

from app.dependencies.db_deps import DBSession
from app.models.user import TokenResponse, UserLogin
from app.services import auth_services as services

from app.core.exceptions import UserNotFound, CredentialsException


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
            key="access_token",
            value=token_data.access_token,
            httponly=True,
            secure=False, #=> True solo para produccion
            samesite="lax"
        )
        return token_data     
    
    except (UserNotFound, CredentialsException):        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Usuario o contraseña incorrectos'
        )      