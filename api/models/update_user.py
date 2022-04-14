from api.models.base_model import BaseModel


class UpdateUser(BaseModel):
    id: str
    method: str
    name: str
    surname: str
    phone: str
    age: int
