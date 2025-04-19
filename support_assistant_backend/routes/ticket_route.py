from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from support_assistant_backend.schemas.ticket import TicketCreate, TicketRead
from support_assistant_backend.schemas.message import MessageCreate, MessageRead
from support_assistant_backend.services.ticket_service import TicketService
from support_assistant_backend.services.message_service import MessageService
from support_assistant_backend.dependencies import get_current_user
from support_assistant_backend.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[TicketRead])
async def list_tickets(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    return await service.list_tickets(str(user.id))

@router.post("/", response_model=TicketRead)
async def create_ticket(ticket_in: TicketCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    return await service.create_ticket(str(user.id), ticket_in)

@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: str, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    ticket = await service.get_ticket(ticket_id)
    if ticket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return ticket

@router.post("/{ticket_id}/messages", response_model=MessageRead)
async def add_message(ticket_id: str, msg_in: MessageCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # ensure ticket ownership
    ticket = await TicketService(db).get_ticket(ticket_id)
    if ticket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = MessageService(db)
    return await service.add_message(ticket_id, msg_in)