from fastapi import APIRouter, Request
from app.core.jinja import templates
from app.models.user import User
from app.dependencies.permission import receptionist_dependency

router = APIRouter()

@router.get('', name='module_receptionist')  # ◄ Ruta final: /admin/receptionist
def get_receptionist(request: Request, current_user: User = receptionist_dependency):
    return templates.TemplateResponse(
        request=request, 
        name='panel/receptionist.html',
        context={"user": current_user}
    )