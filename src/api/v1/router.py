from fastapi import APIRouter

from src.api.v1 import user
from src.api.v1 import auth
from src.api.v1 import document

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(document.router)