from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from .config import settings
from .exceptions import AuthException


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
        return AuthException()
    except jwt.InvalidTokenError as e:
        return AuthException()



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:        
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRES_MIN)

    to_encode.update({"exp": expire})

    # Convertir sub a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)