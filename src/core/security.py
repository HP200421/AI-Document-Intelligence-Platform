import bcrypt #For passwords
import hashlib #For refresh tokens
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from datetime import datetime, timedelta, timezone
import jwt
from src.core.config import settings

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=14)
    password_bytes = password.encode("utf-8")

    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash.decode("utf-8")

def verify_password(password:str, password_hash:str) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes, hash_bytes
    )

def generate_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRY
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def generate_refresh_token(user_id: int) -> str:
     expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRY
        )

     payload = {
         "sub": str(user_id),
         "type":"refresh",
         "exp": expires_at
     }

     refresh_token = jwt.encode(
         payload,
         settings.JWT_SECRET_KEY,
         algorithm=settings.JWT_ALGORITHM
     )

     return refresh_token, expires_at

def hash_refresh_token(refresh_token:str) -> str:
    refresh_token_bytes = refresh_token.encode("utf-8")
    refresh_token_hash = hashlib.sha256(refresh_token_bytes).hexdigest()

    return refresh_token_hash

def decode_token(token:str | None) -> dict[str,any]:
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        if not token:
            raise credentials_exception

        # Decode token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM
        )

        return payload
               
    except (InvalidTokenError, ValueError):
        raise credentials_exception