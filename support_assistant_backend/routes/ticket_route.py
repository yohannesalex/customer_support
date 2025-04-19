# support_assistant_backend/routes/ticket_route.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from support_assistant_backend.schemas.ticket import TicketCreate, TicketRead
from support_assistant_backend.schemas.message import MessageCreate, MessageRead
from support_assistant_backend.services.ticket_service import TicketService
from support_assistant_backend.services.message_service import MessageService
from support_assistant_backend.dependencies import get_current_user, get_current_admin_user
from support_assistant_backend.db.session import get_db

router = APIRouter()

@router.get(
    "/",
    response_model=List[TicketRead],
    status_code=status.HTTP_200_OK,
    summary="List all tickets (admin only)",
    responses={
        200: {"description": "List of all tickets"},
        403: {"description": "Admin privileges required."},
    },
)
async def list_all_tickets(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin_user),
):
    tickets = await TicketService(db).get_all_tickets()
    # Return empty list if no tickets
    return tickets

@router.post(
    "/",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket",
    responses={
        201: {"description": "Ticket created successfully."},
        401: {"description": "Authentication required."},
        422: {"description": "Validation error."},
    },
)
async def create_ticket(
    ticket_in: TicketCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        ticket = await TicketService(db).create_ticket(str(user.id), ticket_in)
        return ticket
    except Exception as e:
        # Log error if needed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{ticket_id}",
    response_model=TicketRead,
    status_code=status.HTTP_200_OK,
    summary="Get a specific ticket",
    responses={
        200: {"description": "Ticket retrieved."},
        401: {"description": "Authentication required."},
        403: {"description": "Not authorized to view this ticket."},
        404: {"description": "Ticket not found."},
    },
)
async def get_ticket(
    ticket_id: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ticket = await TicketService(db).get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found."
        )
    if ticket.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this ticket."
        )
    return ticket

@router.post(
    "/{ticket_id}/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a message to a ticket",
    responses={
        201: {"description": "Message added successfully."},
        401: {"description": "Authentication required."},
        403: {"description": "Not authorized to add message to this ticket."},
        404: {"description": "Ticket not found."},
        422: {"description": "Validation error."},
    },
)
async def add_message(
    ticket_id: str,
    msg_in: MessageCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ticket = await TicketService(db).get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found."
        )
    if ticket.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add message to this ticket."
        )
    try:
        message = await MessageService(db).add_message(ticket_id, msg_in)
        return message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )