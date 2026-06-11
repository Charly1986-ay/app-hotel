from sqlmodel import Session

from app.core.exceptions import EmailExistsException
from app.models.user import User, UserCreate
from app.repository.user_repository import UserRepository
from app.core.security import get_password_hash


def register(user: UserCreate, db: Session) -> User:
    # Normalizar email
    email = user.email.strip().lower()

    user_repository = UserRepository(db=db)

    if user_repository.get_by_email(email):
        raise EmailExistsException()
    
    user_db = User(
        email=email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )

    return user_repository.create(user=user_db)