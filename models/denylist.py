from pydantic import BaseModel


class DenylistOutdb(BaseModel):
    jti: str