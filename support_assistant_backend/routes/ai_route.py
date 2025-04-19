from fastapi import APIRouter, Depends, HTTPException, Response
from support_assistant_backend.services.ai_service import AIService
from support_assistant_backend.dependencies import get_current_user
from support_assistant_backend.services.ticket_service import TicketService
from support_assistant_backend.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/{ticket_id}/ai-response")
async def ai_response(
    ticket_id: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 1. Load the ticket and build your prompt
    ticket = await TicketService(db).get_ticket(ticket_id)
    prompt = f"You are a helpful support assistant. The issue: {ticket.description}\n"

    service = AIService()

    # 2. Consume the async generator directly, accumulating into one string
    full_response = ""
    try:
        async for chunk in service.stream_response(prompt):
            # if chunk is bytes, decode; else assume str
            if isinstance(chunk, (bytes, bytearray)):
                full_response += chunk.decode("utf-8")
            else:
                full_response += str(chunk)

    except Exception as e:
        logger.error("Error while streaming AI response", exc_info=e)
        raise HTTPException(status_code=500, detail="AI service error")

    logger.info(f"AI response for ticket {ticket_id} by user {user.id}: {full_response!r}")

    # 3. Return as plain text (or JSON if you prefer)
    return Response(content=full_response, media_type="text/plain")
