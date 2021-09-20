import uuid
from fastapi import Form
from pydantic import BaseModel, constr
from typing import Optional


class UserInput(BaseModel):
    first_name: str = Form(..., max_length=50)
    last_name: str = Form(..., max_length=50)
    username: str = Form(..., max_length=50)
    password: str = Form(
        ...,
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{4,50}$'
    )
    email: str = Form(
        ...,
        max_length=64,
        regex=r'^([a-zA-Z0-9]+(?:[.-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:[.-]?[a-zA-Z0-9]+)*\.[a-zA-Z]{2,7})$'
    )


class UserInputDb(BaseModel):
    public_id: str
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    is_suspend: bool


class UserUpdateDb(BaseModel):
    first_name: Optional[constr(max_length=50)]
    last_name: Optional[constr(max_length=50)]
