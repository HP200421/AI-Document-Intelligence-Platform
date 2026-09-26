from fastapi import Cookie, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from src.core.config import Settings
from src.core.security import decode_token

def get_current_user(access_token: str | None = Cookie(default=None, alias="access_token")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        if not access_token:
            raise credentials_exception
        
        payload = decode_token(access_token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        if payload.get("type") != "access":
            raise credentials_exception

        return int(user_id)
    except (InvalidTokenError, ValueError):
        raise credentials_exception
