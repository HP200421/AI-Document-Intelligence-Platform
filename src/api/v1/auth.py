from fastapi import APIRouter, Depends, Response, Cookie
from src.schemas.auth import LoginRequest, TokenResponse
from src.services.auth_service import login, refresh_access_token, logout
from sqlalchemy.orm import Session

from src.db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def user_login_endpoint(login_data: LoginRequest, response : Response, db: Session = Depends(get_db)):
    tokens = login(db, login_data)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=604800, #7 Days
    )

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=900, #15 Minutes
    )

    return {"message": "Login successful", "access_token": tokens.access_token, "refresh_token":tokens.refresh_token}

@router.post("/refresh")
def refresh_access_token_endpoint(response:Response, refresh_token:str | None = Cookie(default=None, alias="refresh_token"), db:Session = Depends(get_db)):
    tokens = refresh_access_token(db, refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=604800, #7 Days
    )

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="lax",
        max_age=900, #15 Minutes
    )

    return {"message": "Token refreshed successfully", "access_token": tokens.access_token, "refresh_token":tokens.refresh_token}

@router.post("/logout")
def user_logout_endpoint(response:Response, db:Session = Depends(get_db), refresh_token:str | None = Cookie(default=None, alias="refresh_token")):
    logout(db, refresh_token)
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")

    return {"message": "User logged out successfully"}