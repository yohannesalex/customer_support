# Import necessary modules for building the API router and handling requests.
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# Import Pydantic schemas for request/response data validation.
from support_assistant_backend.schemas.ticket import TicketCreate, TicketRead
from support_assistant_backend.schemas.message import MessageCreate, MessageRead
# Import the service layers for ticket and message logic.
from support_assistant_backend.services.ticket_service import TicketService
from support_assistant_backend.services.message_service import MessageService
# Import dependencies for getting the current authenticated user and the database session.
from support_assistant_backend.dependencies import get_current_user,get_current_admin_user
from support_assistant_backend.db.session import get_db

# Create an API router instance dedicated to ticket and message routes.
router = APIRouter()

# Define endpoints for listing and creating tickets.
# These endpoints require authentication (Depends(get_current_user)) and a database session (Depends(get_db)).
@router.get("/", response_model=List[TicketRead])
async def list_all_tickets(
   db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin_user),     # ← only admin can list all tickets
):
    return await TicketService(db).get_all_tickets()  # admin sees every ticket

@router.post("/", response_model=TicketRead)
async def create_ticket(ticket_in: TicketCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Delegate ticket creation logic to the TicketService.
    service = TicketService(db)
    return await service.create_ticket(str(user.id), ticket_in)

# Define endpoint for retrieving a specific ticket, including an ownership check.
@router.get("/{ticket_id}", response_model=TicketRead)
# Utilizes the database session and authenticated user dependencies.
async def get_ticket(ticket_id: str, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Retrieve ticket using TicketService.
    service = TicketService(db)
    ticket = await service.get_ticket(ticket_id)
    # Ensure the retrieved ticket belongs to the current user.
    if ticket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return ticket

# Define endpoint for adding a message to a specific ticket.
@router.post("/{ticket_id}/messages", response_model=MessageRead)
async def add_message(ticket_id: str, msg_in: MessageCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # ensure ticket ownership before adding a message.
    ticket = await TicketService(db).get_ticket(ticket_id)
    if ticket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Delegate message adding logic to the MessageService.
    service = MessageService(db)
    return await service.add_message(ticket_id, msg_in)