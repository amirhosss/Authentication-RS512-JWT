from fastapi import APIRouter, Depends, Response

from api.dependencies.JWT_config import refresh_token_required
from api.repositories.auth import refresh


router = APIRouter(prefix='/refresh')


@router.post('/web')
async def web_refresh_token(
    response: Response,
    jwt_token: str = Depends(refresh_token_required)
):
    return await refresh.refresh_access_token('web', jwt_token, response)


@router.post('/mobile')
async def mobile_refresh_token(jwt_token: str = Depends(refresh_token_required)):
    return await refresh.refresh_access_token('mobile', jwt_token)