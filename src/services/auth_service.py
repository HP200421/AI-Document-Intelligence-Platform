from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.user_repo import get_user_by_email
from src.schemas.auth import LoginRequest, TokenResponse
from src.core.security import generate_access_token, generate_refresh_token, verify_password, hash_refresh_token, decode_token
from src.repositories.refresh_token_repo import create_refresh_token, get_refresh_token_by_hash, revoke_refresh_token

def login(db:Session, login_data:LoginRequest):
    user = get_user_by_email(db, login_data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email"
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token = generate_access_token(user.id)
    refresh_token, expires_at = generate_refresh_token(user.id)

    # Hash refresh token to store in database table
    refresh_token_hash = hash_refresh_token(refresh_token)
    # Repository operation to create refresh token record
    create_refresh_token(db, refresh_token_hash, user.id, expires_at)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

def refresh_access_token(db:Session, refresh_token:str) -> TokenResponse:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
    )

    # Decode refresh token
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise credentials_exception

    # sub from token
    user_id = payload.get("sub")

    if not user_id:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except(TypeError, ValueError):
        raise credentials_exception

    # Hash refresh token
    refresh_token_hash = hash_refresh_token(refresh_token)

    if not refresh_token_hash:
        raise credentials_exception

    
    # Find the corresponding DB record for refresh token hash
    db_refresh_token = get_refresh_token_by_hash(db, refresh_token_hash)

    if not db_refresh_token:
        raise credentials_exception

    # Check if token has been already revoked
    if db_refresh_token.revoked_at is not None:
        raise credentials_exception

    # Check if token belongs to JWT user
    if db_refresh_token.user_id != user_id:
        raise credentials_exception

    # Revoke refresh token
    revoke_refresh_token(db, db_refresh_token)

    # New access token
    access_token = generate_access_token(user_id)

    # New refresh token
    new_refresh_token, expires_at = generate_refresh_token(user_id)

    # Hash refresh token
    new_refresh_token_hash = hash_refresh_token(new_refresh_token)

    # Create new refresh token record
    create_refresh_token(db,new_refresh_token_hash, user_id, expires_at)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token
    )

def logout(db:Session, refresh_token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if not refresh_token:
        raise credentials_exception

    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise credentials_exception

    user_id = payload.get("sub")

    try:
        user_id = int(user_id)    
    except (TypeError, ValueError):
        raise credentials_exception
    
    refresh_token_hash = hash_refresh_token(refresh_token)

    db_refresh_token = get_refresh_token_by_hash(db, refresh_token_hash)

    if not db_refresh_token:
        raise credentials_exception

    if db_refresh_token.revoked_at is not None:
        raise credentials_exception

    if db_refresh_token.user_id != user_id:
        raise credentials_exception

    revoke_refresh_token(db, db_refresh_token)


    

    




    



