from fastapi import APIRouter, Request
from app.core.jinja import templates
from app.models.user import User
from app.dependencies.permission import supervisor_dependency

router = APIRouter()

@router.get('', name='module_supervisor')
def get_supervisor(
    request: Request, 
    current_user: User = supervisor_dependency
):  
    return templates.TemplateResponse(
        request=request, 
        name='panel/supervisor.html',
        context={"user": current_user} # ◄ Le pasamos el usuario a Jinja por si quieres usarlo en el HTML
    )