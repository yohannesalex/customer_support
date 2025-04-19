from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from support_assistant_backend.models.ticket import Ticket
from support_assistant_backend.schemas.ticket import TicketCreate

class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_tickets(self) -> list[Ticket]:
        result = await self.db.execute(select(Ticket))
        return result.scalars().all()

    async def get_tickets_for_user(self, user_id: str) -> list[Ticket]:
        result = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()

    async def create_ticket(self, user_id: str, ticket_in: TicketCreate) -> Ticket:
        ticket = Ticket(user_id=user_id, **ticket_in.dict())
        try:
            self.db.add(ticket)
            await self.db.commit()
            await self.db.refresh(ticket)
            return ticket
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get_ticket(self, ticket_id: str) -> Ticket | None:
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = result.scalar_one_or_none()
        return ticket
