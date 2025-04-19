from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from support_assistant_backend.services.ai_service import AIService
from support_assistant_backend.dependencies import get_current_user
from support_assistant_backend.services.ticket_service import TicketService
from support_assistant_backend.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/ai-response")
async def ai_response(ticket_id: str, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # fetch ticket and message history
    ticket = await TicketService(db).get_ticket(ticket_id)
    # build prompt
    prompt = f"You are a helpful support assistant. The issue: {ticket.description}\n"
    service = AIService()
    return StreamingResponse(service.stream_response(prompt), media_type="text/event-stream")