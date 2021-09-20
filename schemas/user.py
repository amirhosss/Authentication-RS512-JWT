from pydantic import BaseModel, constr
from typing import Optional


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
