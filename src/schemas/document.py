from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    content_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

