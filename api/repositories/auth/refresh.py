from fastapi import HTTPException, status, Response
from typing import Optional

from api.dependencies.JWT_config import jwt_decode, create_jwt_token
from crud.crud_objects import crud



async def refresh_access_token(
    app_type: str,
    jwt_token: str,
    response: Optional[Response] = None
):
    decoded_public_id = (await jwt_decode(jwt_token, 'refresh'))['public_id']

    if await crud.read(public_id=decoded_public_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    access_payload = {'public_id': decoded_public_id, 'aud': 'access'}
    access_token = create_jwt_token(access_payload)

    if app_type == 'web':
        response.set_cookie(key='access_token', value=access_token)

        return {'detail': 'Access token refreshed successfully'}

    return {
        'detail': 'Access token refreshed successfully',
        'access_token': access_token
    }