from typing import Optional

from api.models.base_model import BaseModel


class SelectUserRequest(BaseModel):
    id: str
    method: str
    name: Optional[str]
    surname: Optional[str]
    phone: Optional[str]
