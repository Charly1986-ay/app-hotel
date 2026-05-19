from fastapi import Request
from jwt import PyJWTError

from app.core.security import verify_access_token

from app.core.jinja import templates


async def auth_middleware(request: Request, call_next):

    token = request.cookies.get("access_token")    
    
    if token:
        try:
            payload = verify_access_token(token=token)

            sub = payload.get("sub")

            #print(f'{type(sub)} => id: {sub}')

            if sub:
                request.state.user_id = sub

        except PyJWTError as e:           
            print("JWT ERROR:", e)  

    response = await call_next(request)
    return response