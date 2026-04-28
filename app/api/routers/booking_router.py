from sys import prefix

from fastapi import Request
from fastapi.routing import APIRouter
from app.core.jinja import templates


router = APIRouter()

@router.get('/')
def get_index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='index.html'
        # context={"id": id} => aca va los parametros
    )