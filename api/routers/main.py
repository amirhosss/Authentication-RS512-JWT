from fastapi import APIRouter

from .user import user
from .auth import auth


router = APIRouter(
    prefix='/api'
)

router.include_router(user.router)
router.include_router(auth.router)