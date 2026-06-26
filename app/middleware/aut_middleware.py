from fastapi import Request
from app.core.exceptions import CredentialsException, ExpiredTokenException
from app.core.security import verify_access_token
from app.core.jinja import templates


async def auth_middleware(request: Request, call_next):    
    if request.scope.get("type") == "websocket" or request.url.path.startswith("/ws"):
        return await call_next(request)

    # --- El resto de tu lógica HTTP se queda exactamente igual ---
    token = request.cookies.get("access_token")    
    
    if token:
        try:
            # Operación en memoria/CPU, se ejecuta de forma directa
            payload = verify_access_token(token=token)
            sub = payload.get("sub")

            if sub:
                # Seteamos el user_id en el estado para que 'permission.py' lo lea
                request.state.user_id = sub

        # CORRECCIÓN: Atrapamos tus excepciones reales del sistema de seguridad
        except (CredentialsException, ExpiredTokenException) as e:           
            print("JWT AUTH MIDDLEWARE ERROR: Token inválido o expirado.")  
        except Exception as e:
            print("JWT AUTH MIDDLEWARE ERROR inesperado:", e)

    # El flujo asíncrono aquí es impecable, continúa al siguiente componente
    response = await call_next(request)
    return response