from api.models.base_model import BaseModel


class TesterResponse(BaseModel):
    attribute_type_map = {
        'id': str,
        'method': str,
        'status': str,
        'reason': str
    }
