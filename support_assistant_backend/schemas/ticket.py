from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from .message import MessageRead

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketRead(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    created_at: datetime
    messages: List[MessageRead] = []

    class Config:
        orm_mode = True