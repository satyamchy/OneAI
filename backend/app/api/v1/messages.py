from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.message import MessageCreate, MessageListResponse, MessageResponse, StreamMessageCreate
from app.services.chat_service import stream_chat_response
from app.services.conversation_service import get_conversation
from app.services.message_service import create_message, list_messages
from app.core.constants import MessageRole
from app.utils.request_id import generate_request_id

router = APIRouter(prefix="/conversations/{conversation_id}/messages", tags=["messages"])

# Lists messages for a conversation owned by the authenticated user.
@router.get("", response_model=MessageListResponse)
async def get_messages(conversation_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await get_conversation(db, user, conversation_id)
    return MessageListResponse(request_id=generate_request_id(), messages=await list_messages(db, conversation_id))

# Creates a non-streaming message record for a conversation.
@router.post("", response_model=MessageResponse)
async def post_message(conversation_id: UUID, payload: MessageCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await get_conversation(db, user, conversation_id)
    message = await create_message(db, conversation_id, payload.role, payload.content)
    return MessageResponse(request_id=generate_request_id(), message=message)

# Streams a mode-aware assistant response for the next user message.
@router.post("/stream")
async def stream_message(conversation_id: UUID, payload: StreamMessageCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    request_id = generate_request_id()
    conversation = await get_conversation(db, user, conversation_id)
    stream = stream_chat_response(db, conversation, user.id, payload.content, payload.model, payload.mode, request_id)
    return StreamingResponse(stream, media_type="text/event-stream", headers={"X-Request-ID": request_id})
