from fastapi import HTTPException, status

from api.dependencies.JWT_config import jwt_decode
from crud.crud_objects import crud, denylist_crud

async def verify_user(verify_token: str):
    decoded_jwt = await jwt_decode(verify_token, 'verification')

    decoded_public_id = decoded_jwt['public_id']
    decoded_jti = decoded_jwt['jti']

    user = await crud.read(is_admin=True, public_id=decoded_public_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    elif not user.is_suspend:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='User already verified'
        )

    await denylist_crud.create({'jti': decoded_jti})

    await crud.update({'is_suspend': False}, public_id=decoded_public_id)

    return {'detail': 'User activated successfully'}