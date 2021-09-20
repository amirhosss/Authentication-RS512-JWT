from fastapi import HTTPException, status

from crud.crud_objects import crud


async def check_user_inDb(public_id: str):
    if (user := await crud.read(is_admin=True, public_id=str(public_id))) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    return user