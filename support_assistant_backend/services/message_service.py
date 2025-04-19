from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.models.message import Message
from support_assistant_backend.schemas.message import MessageCreate

class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, ticket_id: str, msg_in: MessageCreate, is_ai: bool = False):
        message = Message(ticket_id=ticket_id, content=msg_in.content, is_ai=is_ai)
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message