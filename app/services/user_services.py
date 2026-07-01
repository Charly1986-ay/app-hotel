from fastapi import BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import EmailExistsException
from app.models.user import User, UserCreate
from app.repository.user_repository import UserRepository
from app.core.security import get_password_hash
from app.services.mail_services import generate_welcome_html, send_email_base


async def register(user: UserCreate, db: AsyncSession, background_tasks: BackgroundTasks) -> User:    
    email = user.email.strip().lower()

    user_repository = UserRepository(db=db)
   
    if await user_repository.get_by_email(email):
        raise EmailExistsException()
    
    # El hasheo de contraseñas ocurre puramente en la CPU, se mantiene sincrónico
    user_db = User(
        email=email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    
    user_created = await user_repository.create(user=user_db)
    
    html_content = generate_welcome_html(user_name=user_created.full_name)
    
    # Encolar la tarea de fondo sigue funcionando exactamente igual
    background_tasks.add_task(
        send_email_base,
        email_destination=user_created.email,
        subject="¡Bienvenido a Hotel Management System! 🏨",
        body_html=html_content
    )

    return user_created