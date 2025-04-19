from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.models.ticket import Ticket
from support_assistant_backend.schemas.ticket import TicketCreate

class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tickets(self, user_id: str):
        # Fetch all tickets associated with a specific user ID.
        result = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()

    async def create_ticket(self, user_id: str, ticket_in: TicketCreate):
        # Create a new Ticket object with the provided data.
        ticket = Ticket(user_id=user_id, **ticket_in.dict())
        # Add the new ticket to the database session.
        self.db.add(ticket)
        # Commit the changes to persist the ticket in the database.
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def get_ticket(self, ticket_id: str):
        # Retrieve a specific ticket based on its ID.
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one()