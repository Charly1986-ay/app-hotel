from fastapi import Depends, Request
from sqlmodel import Session

from app.core.exceptions import CredentialsException, UserInactiveException, ForbiddenException
from app.dependencies.db_deps import DBSession
from app.models.user import Role, User, UserStatus
from .auth_deps import require_auth

from app.repository.user_repository import UserRepository


def get_token_user_id(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise CredentialsException()
    return user_id


def get_current_user(user_id: int = Depends(get_token_user_id), db: Session = DBSession) -> User:
    user_repository = UserRepository(db=db)
    
    user = user_repository.get(user_id=user_id)
    if not user:
        raise CredentialsException()
    return user


def get_current_user_active(user = Depends(get_current_user)) -> User:
    if user.status == UserStatus.INACTIVE:
        raise UserInactiveException()
    return user


def require_roles(*allowed_roles: Role):
    def role_checker(user: User = Depends(get_current_user_active)) -> User:
        if user.role not in allowed_roles:
            raise ForbiddenException()
        return user
    return role_checker


# Solo recepcionistas
receptionist_dependency = Depends(require_roles(Role.RECEPTIONIST))

# Solo supervisores
supervisor_dependency = Depends(require_roles(Role.SUPERVISOR))

# Manager o supervisor (por ejemplo)
manager_or_supervisor = Depends(require_roles(Role.MANAGER, Role.SUPERVISOR))