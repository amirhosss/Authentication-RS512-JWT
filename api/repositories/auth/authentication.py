from fastapi import (
    Response,
    BackgroundTasks,
    HTTPException,
    status
)
from datetime import timedelta
from typing import Optional

from crud.crud_objects import crud
from api.dependencies.JWT_config import create_jwt_token
from core.hashing_password import verify_password
from api.utils.sending_email import send_email


async def authenticate_user(
    app_type: str,
    background_task: BackgroundTasks,
    username: str,
    password: str,
    response: Optional[Response] = None
):
    if not (document := await crud.read(is_admin=True, username=username)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wrong username or password'
        )

    hashed_password = document.password
    if not verify_password(password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wrong username or password'
        )

    if document.is_suspend:
        verify_jwt = create_jwt_token(
            {'aud': 'verification', 'public_id': document.public_id},
            timedelta(minutes=5)
        )

        verification_link = f'http://localhost:8000/api/auth/verification?verify_token={verify_jwt}'
        email_content = f'This is your verification link.\n{verification_link}'

        background_task.add_task(
            send_email,
            email=document.email,
            subject='Email verification',
            content=email_content
        )

        return {'detail': 'An email sent to your account, you have 5 minutes to verify it'}

    access_payload = {'public_id': document.public_id, 'aud': 'access'}
    refresh_payload = {'public_id': document.public_id, 'aud': 'refresh'}

    access_token = create_jwt_token(access_payload)
    refresh_token = create_jwt_token(refresh_payload, timedelta(days=30))

    if app_type == 'web':
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        return {'detail': 'User authenticated successfully'}

    return {
        'detail': 'User authenticated successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
    }