from crud.crud_objects import denylist_crud
from api.dependencies.JWT_config import jwt_decode


async def revoke_access_token(jwt_token: str):
    decoded_jti= (await jwt_decode(jwt_token, 'access')).get('jti')
    await denylist_crud.create({'jti': decoded_jti})

    return {'detail': 'Access token revoked successfully'}


async def revoke_refresh_token(jwt_token: str):
    decoded_jti = (await jwt_decode(jwt_token, 'refresh'))['jti']
    await denylist_crud.create({'jti': decoded_jti})

    return {'detail': 'Refresh token revoked successfully'}