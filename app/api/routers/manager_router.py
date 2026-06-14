from fastapi import APIRouter, Request
from app.core.jinja import templates
from app.models.user import User
from app.dependencies.permission import manager_dependency

router = APIRouter()

@router.get('', name='module_manager')  # ◄ Ruta final: /admin/manager
def get_manager(request: Request, current_user: User = manager_dependency):
    return templates.TemplateResponse(
        request=request, 
        name='panel/manager.html',
        context={"user": current_user}
    )