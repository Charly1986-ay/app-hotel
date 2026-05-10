from fastapi import Request

from app.core.security import verify_access_token

from app.core.jinja import templates


async def auth_middleware(request: Request, call_next):
    request.state.user_id = None

    token = request.cookies.get('access_token')

    if token:
        try:
            payload = verify_access_token(token=token)
            request.state.user_id = int(payload["sub"])

        except Exception:
            pass
    
    response = await call_next(request)    

    return response