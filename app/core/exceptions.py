from fastapi import HTTPException, status


class AuthException(HTTPException):
    """Excepción genertica de autenticación."""
    def __init__(self, detail: str = "Usuario no autenticado o credencial inválida"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail
    )
        

class UserInactiveException(HTTPException):
    """Excepción que ocurre cuando un usuario está inactivo."""
    def __init__(self, detail: str = "Usuario inactivo"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=detail
    )