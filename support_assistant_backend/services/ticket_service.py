from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.models.ticket import Ticket
from support_assistant_backend.schemas.ticket import TicketCreate

class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tickets(self, user_id: str):
        result = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()

    async def create_ticket(self, user_id: str, ticket_in: TicketCreate):
        ticket = Ticket(user_id=user_id, **ticket_in.dict())
        self.db.add(ticket)
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def get_ticket(self, ticket_id: str):
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one()