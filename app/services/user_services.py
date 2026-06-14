from fastapi import BackgroundTasks
from sqlmodel import Session

from app.core.exceptions import EmailExistsException
from app.models.user import User, UserCreate
from app.repository.user_repository import UserRepository
from app.core.security import get_password_hash
from app.services.mail_services import generate_welcome_html, send_email_base


def register(user: UserCreate, db: Session, background_tasks: BackgroundTasks) -> User:
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

    # Guardamos en la base de datos
    user_created = user_repository.create(user=user_db)

    # Encolamos el correo para que no trabe la experiencia del cliente online
    html_content = generate_welcome_html(user_name=user_created.full_name)
    background_tasks.add_task(
        send_email_base,
        email_destination=user_created.email,
        subject="¡Bienvenido a Hotel Management System! 🏨",
        body_html=html_content
    )

    return user_created