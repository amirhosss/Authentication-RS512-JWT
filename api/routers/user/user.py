import uuid
from fastapi import (
    APIRouter,
    status,
    Body,
    Response,
    Depends,
    BackgroundTasks
)

import api.repositories.users.user as user_repo
from schemas.user import UserUpdateDb
from models.user import UserOutDb
from api.dependencies.authorize_user import authorize_current_user
from api.dependencies.check_user import check_user_inDb
from api.dependencies.user_input import UserInput
from api.dependencies.JWT_config import refresh_token_required


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def signup_user(
    background_task: BackgroundTasks,
    input_forms=Depends(UserInput)
):
    return await user_repo.signup_user(background_task, input_forms)


@router.get(
    '/{public_id}',
    response_model=UserOutDb,
    dependencies=[Depends(authorize_current_user)]
)
async def get_user(user = Depends(check_user_inDb)):
    return await user_repo.get_user(user)


@router.put(
    '/{public_id}/update',
    dependencies=[Depends(authorize_current_user), Depends(check_user_inDb)]
)
async def modify_user(public_id: uuid.UUID, items: UserUpdateDb = Body(...)):
    return await user_repo.modify_user(public_id, items)


@router.delete('/{public_id}/delete')
async def remove_user(
    response: Response,
    public_id: uuid.UUID,
    jwt_token: str = Depends(refresh_token_required)
):
    return await user_repo.remove_user(public_id, jwt_token, response)
