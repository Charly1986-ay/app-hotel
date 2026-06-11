from fastapi import HTTPException, status


class CredentialsException(HTTPException):
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
        

class ExpiredTokenException(HTTPException):
    """Excepción específica para token expirado."""
    def __init__(self, detail: str = "Token expirado, inicia sesión nuevamente"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class ForbiddenException(HTTPException):
    """Excepción lanzada cuando un usuario itenta acceder a un recurso que no tiene permiso."""
    def __init__(self, detail: str = "No tienes permisos para acceder a este recurso"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=detail
    )
        

class UserNotFound(HTTPException):
    """Excepción lanzada cuando un usuario no es encontrado en base de datos."""
    def __init__(self, detail: str = "Usuario no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )
        

class EmailExistsException (HTTPException):
    """Excepción se produce cuando el email existe en la base de datos."""
    def __init__(self, detail: str = "Email ya existe en la base de datos"):
        super().__init__(status_code=409, detail=detail)


class PaymentException(HTTPException):
    """Excepción lanzada cuando el pago no pudo ser realizado."""
    def __init__(self, detail: str = "El pago no pudo ser realizado. Verifique los datos"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, 
            detail=detail
    )
        

class RoomNotFound(HTTPException):
    """Excepción lanzada cuando no encuentra habitaciones en la base de datos."""
    def __init__(self, detail: str = "Habitaciones inválidas o no encontradas"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
    )
        

class PriceMismatchException(HTTPException):
    """Excepción lanzada cuando el precio de la habitaciones no coincide con la base de datos."""
    def __init__(self, detail: str = "Precio de la habitación desactualizada"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, 
            detail=detail
    )