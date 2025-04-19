from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: UUID
    content: str
    is_ai: bool
    created_at: datetime

    class Config:
        orm_mode = True 