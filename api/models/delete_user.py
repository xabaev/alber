from api.models.base_model import BaseModel


class DeleteUser(BaseModel):
    id: str
    method: str
    phone: str
