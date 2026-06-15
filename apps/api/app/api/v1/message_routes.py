from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.dependencies import CurrentUser, DbSession
from app.core.logging import get_request_id
from app.schemas.message import MessageRead, MessageStreamRequest
from app.services.chat.chat_orchestrator import ChatOrchestrator
from app.services.message_service import MessageService

router = APIRouter()


@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
async def list_messages(
    conversation_id: str,
    db: DbSession,
    user: CurrentUser,
) -> list[MessageRead]:
    messages = await MessageService(db).list_for_conversation(conversation_id, user)
    return [MessageRead.model_validate(message) for message in messages]


@router.post("/{conversation_id}/messages/stream")
async def stream_message(
    conversation_id: str,
    payload: MessageStreamRequest,
    db: DbSession,
    user: CurrentUser,
) -> StreamingResponse:
    generator = ChatOrchestrator(db).stream_message(
        conversation_id=conversation_id,
        payload=payload,
        user=user,
        request_id=get_request_id(),
    )
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

