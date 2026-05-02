from fastapi import Request
from fastapi.routing import APIRouter
from app.core.jinja import templates


router = APIRouter()

@router.get('', name='account_user')
def get_index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='register.html'        
    )