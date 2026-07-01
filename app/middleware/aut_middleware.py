from fastapi import Request, logger
from app.core.exceptions import CredentialsException, ExpiredTokenException
from app.core.security import verify_access_token


async def auth_middleware(request: Request, call_next):    
    # Extraemos el token desde las cookies
    token = request.cookies.get("access_token")    
    
    if token:
        try:
            # Operación en memoria/CPU, se ejecuta de forma directa
            payload = verify_access_token(token=token)
            sub = payload.get("sub")

            if sub:
                # Seteamos el user_id en el estado para que 'permission.py' lo lea
                request.state.user_id = sub

        # Atrapamos tus excepciones reales del sistema de seguridad
        except (CredentialsException, ExpiredTokenException):           
            pass
        except Exception as e:
            logger.error(f"Error inesperado en JWT Middleware: {e}", exc_info=True)

    # Continúa al siguiente componente de la petición HTTP
    return await call_next(request)