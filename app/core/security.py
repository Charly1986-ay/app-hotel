from datetime import datetime, timedelta, timezone
from enum import Enum
import jwt
from pwdlib import PasswordHash
from .config import settings
from .exceptions import CredentialsException, ExpiredTokenException


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError as e:
        raise CredentialsException()



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crea un JWT firmado. 
    Convierte automáticamente Enums a strings y asegura que 'sub' sea string.
    """
    to_encode = data.copy()
    
    # 1. Definir tiempo de expiración
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:         
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRES_MIN)

    # 2. Limpieza y serialización de datos
    for key, value in to_encode.items():
        # Si es un Enum (como tu Role), extraemos el valor real ("admin", "manager")
        if isinstance(value, Enum):
            to_encode[key] = value
        # El estándar JWT prefiere que el 'sub' (User ID) sea string
        elif key == "sub":
            to_encode[key] = str(value)

    # 3. Añadir el claim de expiración
    to_encode.update({"exp": expire})

    # 4. Generar el token firmado
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALG
    )
    
    return encoded_jwt