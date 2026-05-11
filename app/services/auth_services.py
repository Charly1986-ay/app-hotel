from sqlmodel import Session

from app.core.security import verify_password, create_access_token
from app.models.user import TokenResponse, UserLogin
from app.repository.user_repository import UserRepository
from app.core.exceptions import CredentialsException, UserNotFound


def login_services(user: UserLogin, db: Session):
    repository = UserRepository(db=db)

    db_user = repository.get_by_email(email=user.email)

    if not db_user:
        raise UserNotFound()
    
    if not verify_password(
        plain_password=user.password, 
        hashed_password=db_user.hashed_password
    ):
        raise CredentialsException()
    
    access_token = create_access_token(data={
        "sub": db_user.id,
        'role': db_user.role
    })

    return TokenResponse(access_token=access_token, role=db_user.role)