from fastapi import BackgroundTasks
# 1. Cambiamos al tipo de sesión asíncrona
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import EmailExistsException
from app.models.user import User, UserCreate
from app.repository.user_repository import UserRepository
from app.core.security import get_password_hash
from app.services.mail_services import generate_welcome_html, send_email_base


# 2. Convertimos el servicio a 'async def' y tipamos con AsyncSession
async def register(user: UserCreate, db: AsyncSession, background_tasks: BackgroundTasks) -> User:
    # Normalizar email (operación local en memoria)
    email = user.email.strip().lower()

    user_repository = UserRepository(db=db)

    # 3. CRÍTICO: Agregamos 'await' para la consulta de email duplicado
    if await user_repository.get_by_email(email):
        raise EmailExistsException()
    
    # El hasheo de contraseñas ocurre puramente en la CPU, se mantiene sincrónico
    user_db = User(
        email=email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )

    # 4. CRÍTICO: Agregamos 'await' para la inserción del nuevo usuario
    user_created = await user_repository.create(user=user_db)

    # Preparación del molde HTML (operación local en memoria)
    html_content = generate_welcome_html(user_name=user_created.full_name)
    
    # Encolar la tarea de fondo sigue funcionando exactamente igual
    background_tasks.add_task(
        send_email_base,
        email_destination=user_created.email,
        subject="¡Bienvenido a Hotel Management System! 🏨",
        body_html=html_content
    )

    return user_created