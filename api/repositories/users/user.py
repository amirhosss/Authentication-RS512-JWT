import uuid
from fastapi import (
    BackgroundTasks,
    HTTPException,
    status,
    Body,
    Response,
    Depends
)
from datetime import timedelta

from schemas.user import UserInputDb, UserUpdateDb
from crud.crud_objects import crud, denylist_crud
from core.hashing_password import get_password
from api.dependencies.JWT_config import create_jwt_token, jwt_decode
from api.dependencies.user_input import UserInput
from api.utils.sending_email import send_email


async def signup_user(
    background_task: BackgroundTasks,
    input_forms: UserInput = Depends(UserInput)
):
    if await crud.read(username=input_forms.username):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Username already exists'
        )
    if await crud.read(email=input_forms.email):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Email already exists'
        )

    user = UserInputDb(
        public_id=str(uuid.uuid4()),
        first_name=input_forms.first_name,
        last_name=input_forms.last_name,
        username=input_forms.username,
        password=get_password(input_forms.password),
        email=input_forms.email,
        is_suspend=True
    )
    await crud.create(user.dict())

    verify_jwt = create_jwt_token(
        {'aud': 'verification', 'public_id': user.public_id},
        timedelta(minutes=5)
    )
    verification_link = f'http://localhost:8000/api/auth/verification?verify_token={verify_jwt}'
    email_content = f'This is your verification link.\n{verification_link}'

    background_task.add_task(
        send_email,
        email=input_forms.email,
        subject='Email verification',
        content=email_content
    )

    return {'detail': 'An email sent to your account, you have 5 minutes to verify it'}


async def get_user(user):
    return user


async def modify_user(public_id: str, items: UserUpdateDb = Body(...)):
    filtered_items = [(key, value) for key, value in items.dict().items() if value is not None]
    await crud.update(dict(filtered_items), public_id=str(public_id))

    return {'detail': 'User updated successfully'}


async def remove_user(public_id: str, jwt_token: str, response: Response):
    decoded_jwt = await jwt_decode(jwt_token, 'refresh')

    decoded_public_id = decoded_jwt['public_id']
    if str(public_id) != str(decoded_public_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Informations does not match',
            headers={"WWW-Authenticate": "Bearer"}
        )

    if (user := await crud.read(public_id=str(public_id))) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    await crud.delete(public_id=str(public_id))

    decoded_jti =  decoded_jwt['jti']
    await denylist_crud.create({'jti': decoded_jti})

    try:
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
    except Exception as e:
        print(f'Cannot delete cookie cause of {e}')

    return {'detail': 'User deleted successfully'}
