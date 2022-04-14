from api.models.base_model import BaseModel


class AddUser(BaseModel):
    attribute_type_map = {
        'id': str,
        'method': str,
        'name': str,
        'surname': str,
        'phone': str,
        'age': int
    }
