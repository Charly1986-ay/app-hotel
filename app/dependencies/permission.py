from fastapi import Depends, Request

from app.core.exceptions import CredentialsException, UserInactiveException, ForbiddenException
from app.dependencies.db_deps import DBSession
from app.models.user import Role, User, UserStatus
from app.repository.user_repository import UserRepository


def get_token_user_id(request: Request) -> int:
    # Leer del request.state es inmediato en memoria RAM, se queda 'def'
    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        raise CredentialsException()

    try:
        return int(user_id)
    except (TypeError, ValueError):
        raise CredentialsException()


# CORRECCIÓN: Pasa a ser 'async def' porque consulta a la DB asíncrona
async def get_current_user(
        db: DBSession,
        user_id: int = Depends(get_token_user_id)
) -> User:
    user_repository = UserRepository(db=db)
    
    # Agregamos el 'await' obligatorio para extraer el usuario de forma no bloqueante
    user = await user_repository.get(user_id=user_id)
    if not user:
        raise CredentialsException()
    return user


# Práctica recomendada: Al depender de una función async, la volvemos async def
async def get_current_user_active(user: User = Depends(get_current_user)) -> User:
    if user.status == UserStatus.INACTIVE:
        raise UserInactiveException()
    return user


def require_roles(*allowed_roles: Role):
    # Volvemos asíncrona la función interna para acoplarse al flujo de dependencias
    async def role_checker(user: User = Depends(get_current_user_active)) -> User:
        # Extraemos correctamente el .value del Enum de roles tal como lo diseñaste
        if user.role not in [r.value for r in allowed_roles]:
            raise ForbiddenException()
        return user
    return role_checker


# --- Tus Atajos de Dependencias (Siguen funcionando exactamente igual) ---

# Solo clientes
user_dependency = Depends(require_roles(Role.CLIENT))

# Solo recepcionistas
receptionist_dependency = Depends(require_roles(Role.RECEPTIONIST))

# Solo supervisores
supervisor_dependency = Depends(require_roles(Role.SUPERVISOR))

# Solo Manager
manager_dependency = Depends(require_roles(Role.MANAGER))

# Manager o supervisor
manager_or_supervisor = Depends(require_roles(Role.MANAGER, Role.SUPERVISOR))