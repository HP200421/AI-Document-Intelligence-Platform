from src.repositories.user_repo import create_user as create_user_repo
from src.repositories.user_repo import get_users as get_users_repo

from src.models.user import User
from src.schemas.user import UserCreate

from sqlalchemy.orm import Session

# Password Hashing
from src.core.security import hash_password

def create_user(db:Session, user_data:UserCreate) -> User:
    password_hash = hash_password(user_data.password)
    
    return create_user_repo(db, user_data, password_hash)

def get_users(db:Session) -> list[User]:
    return get_users_repo(db)