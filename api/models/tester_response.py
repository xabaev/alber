from typing import Optional

from api.models.base_model import BaseModel


class TesterResponse(BaseModel):
    id: str
    method: str
    status: str
    reason: Optional[str] = None
