from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.core.constants import InteractionMode

class ConversationCreate(BaseModel):
    title: str | None = None
    selected_model: str | None = None
    interaction_mode: InteractionMode = InteractionMode.CHAT

class ConversationUpdate(BaseModel):
    title: str | None = None
    selected_model: str | None = None
    interaction_mode: InteractionMode | None = None
    is_archived: bool | None = None

class ConversationRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    selected_model: str
    interaction_mode: InteractionMode
    created_at: datetime
    updated_at: datetime
    is_archived: bool

    model_config = {"from_attributes": True}

class ConversationListResponse(BaseModel):
    request_id: str
    conversations: list[ConversationRead]

class ConversationResponse(BaseModel):
    request_id: str
    conversation: ConversationRead
