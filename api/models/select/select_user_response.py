from typing import List

from api.models.base_model import BaseModel
from api.models.select.select_user import SelectUser


class SelectUserResponse(BaseModel):
    attribute_type_map = {
        'id': str,
        'method': str,
        'status': str,
        'users': list[SelectUser]
    }
