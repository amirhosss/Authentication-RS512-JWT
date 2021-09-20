from pydantic import BaseModel


class UserOutDb(BaseModel):
    public_id: str
    first_name: str
    last_name: str
    username: str
    email: str


class AdminOutDb(UserOutDb):
    password: str
    is_suspend: bool
