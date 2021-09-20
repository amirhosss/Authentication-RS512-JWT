from fastapi import Response

from api.dependencies.JWT_config import jwt_decode
from crud.crud_objects import denylist_crud


async def logout_user(response: Response, jwt_token: str):
    decoded_jti = (await jwt_decode(jwt_token, 'refresh'))['jti']
    await denylist_crud.create({'jti': decoded_jti})

    response.delete_cookie(key='refresh_token')
    response.delete_cookie(key='access_token')

    return {'detail': 'Web user logged out successfully'}
