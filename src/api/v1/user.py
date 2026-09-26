from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.user import UserCreate, UserResponse
from src.services.user_service import create_user, get_users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data:UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.get("/", response_model=list[UserResponse],)
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

