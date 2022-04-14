from api.models.base_model import BaseModel


class SelectUser(BaseModel):
    attribute_type_map = {
        'name': str,
        'surname': str,
        'phone': str,
        'age': int
    }