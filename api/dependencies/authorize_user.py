import uuid
from fastapi import Depends, HTTPException, status

from .JWT_config import access_token_required, jwt_decode

async def authorize_current_user(
    public_id: uuid.UUID,
    jwt_token: str = Depends(access_token_required)
):
    decoded_public_id = (await jwt_decode(jwt_token, 'access'))['public_id']
    if str(public_id) != str(decoded_public_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Informations does not match',
            headers={"WWW-Authenticate": "Bearer"}
        )