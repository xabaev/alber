from typing import Optional

from api.models.base_model import BaseModel


class SelectUser(BaseModel):
    name: str
    surname: str
    phone: str
    age: int


class SelectUserResponse(BaseModel):
    id: str
    method: str
    status: str
    users: Optional[list[SelectUser]] = None
