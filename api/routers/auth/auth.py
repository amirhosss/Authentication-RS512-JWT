from fastapi import (
    APIRouter,
    Response,
    Depends
)

from api.repositories.auth import revoke, verification, logout
from api.dependencies.JWT_config import access_token_required, refresh_token_required
from . import authentication, refresh


router = APIRouter(
    prefix='/auth',
    tags=['Auth'])

router.include_router(authentication.router)
router.include_router(refresh.router)


@router.delete('/logout')
async def logout_user(
    response: Response,
    jwt_token: str = Depends(refresh_token_required)
):
    return await logout.logout_user(response, jwt_token)


@router.get('/verification')
async def verify_user(verify_token: str):
    return await verification.verify_user(verify_token)


@router.delete('/access-revoke')
async def revoke_access_token(jwt_token: str = Depends(access_token_required)):
    return await revoke.revoke_access_token(jwt_token)


@router.delete('/refresh-revoke')
async def revoke_refresh_token(jwt_token: str = Depends(refresh_token_required)):
    return await revoke.revoke_refresh_token(jwt_token)