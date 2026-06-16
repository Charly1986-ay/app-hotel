# 1. Cambiamos al tipo de sesión asíncrona
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import verify_password, create_access_token
from app.models.user import TokenResponse, UserLogin
from app.repository.user_repository import UserRepository
from app.core.exceptions import CredentialsException, UserNotFound


# 2. Convertimos la función a asíncrona y tipamos con AsyncSession
async def login_services(user: UserLogin, db: AsyncSession) -> TokenResponse:
    repository = UserRepository(db=db)

    # 3. Agregamos el await obligatorio para la consulta a la base de datos
    db_user = await repository.get_by_email(email=user.email)

    if not db_user:
        raise UserNotFound()
    
    # Las funciones de security (verify_password y create_access_token)
    # siguen siendo sincrónicas (operan en CPU/RAM), por lo que NO llevan await.
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