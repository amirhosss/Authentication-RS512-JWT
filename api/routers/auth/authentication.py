from fastapi import APIRouter, Form, BackgroundTasks, Response

from api.repositories.auth import authentication


router = APIRouter(prefix='/authentication')


@router.post('/web')
async def web_authentication(
    response: Response,
    background_task: BackgroundTasks,
    username: str = Form(..., max_length=50),
    password: str = Form(..., max_length=50)
):
    return await authentication.authenticate_user(
        'web',
        background_task,
        username,
        password,
        response
    )


@router.post('/mobile')
async def mobile_authentication(
    background_task: BackgroundTasks,
    username: str = Form(..., max_length=50),
    password: str = Form(..., max_length=50)
):
    return await authentication.authenticate_user(
        'mobile',
        background_task,
        username,
        password
    )