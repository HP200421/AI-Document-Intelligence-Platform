from fastapi import APIRouter

from src.api.v1 import user
from src.api.v1 import auth

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)