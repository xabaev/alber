from api.models.base_model import BaseModel


class DeleteUser(BaseModel):
    attribute_type_map = {
        'id': str,
        'method': str,
        'phone': str,
    }
