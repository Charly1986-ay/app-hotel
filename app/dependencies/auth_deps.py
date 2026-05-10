from fastapi import Request, HTTPException

from app.core.exceptions import AuthException


def require_auth(request: Request):
    user_id = request.state.user_id

    if not user_id:
        raise AuthException()

    return user_id