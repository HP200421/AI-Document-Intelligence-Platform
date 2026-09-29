from src.repositories.user_repo import create_user as create_user_repo
from src.repositories.user_repo import get_users as get_users_repo, get_user_by_email
from fastapi import HTTPException, status
from src.models.user import User
from src.schemas.user import UserCreate

from sqlalchemy.orm import Session

# Password Hashing
from src.core.security import hash_password

def create_user(db:Session, user_data:UserCreate) -> User:
    user_exists = get_user_by_email(db, user_data.email)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    password_hash = hash_password(user_data.password)
    
    return create_user_repo(db, user_data, password_hash)

def get_users(db:Session) -> list[User]:
    return get_users_repo(db)