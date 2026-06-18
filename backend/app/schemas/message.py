from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.core.constants import InteractionMode, MessageRole

class MessageCreate(BaseModel):
    content: str
    role: MessageRole = MessageRole.USER

class StreamMessageCreate(BaseModel):
    content: str
    model: str | None = None
    mode: InteractionMode | None = None

class MessageRead(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    model_used: str | None = None
    mode_used: InteractionMode | None = None
    tool_calls_json: dict | None = None
    search_sources_json: list | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

class MessageListResponse(BaseModel):
    request_id: str
    messages: list[MessageRead]

class MessageResponse(BaseModel):
    request_id: str
    message: MessageRead
