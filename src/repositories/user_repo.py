from src.models.user import User
from src.schemas.user import UserCreate

from sqlalchemy.orm import Session
from sqlalchemy import Select

def create_user(db:Session, user_data:UserCreate, password_hash:str) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash = password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db:Session) -> list[User]:
    statement = Select(User)

    result = db.scalars(statement)

    return list(result.all())

def get_user_by_email(db:Session, email:str) -> User | None:
    statement = Select(User).where(
        User.email == email
    )

    return db.scalar(statement)

