from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class MessageRead(ORMModel):
    id: UUID
    conversation_id: UUID
    user_id: UUID
    role: str
    content: str
    content_json: dict | None
    model_id: str | None
    provider: str | None
    model_run_id: UUID | None
    parent_message_id: UUID | None
    metadata_json: dict
    created_at: datetime


class MessageStreamRequest(BaseModel):
    content: str = Field(min_length=1, max_length=20000)
    model_id: str | None = Field(default=None, max_length=160)
    temperature: float | None = Field(default=0.7, ge=0, le=2)
    max_tokens: int | None = Field(default=1200, ge=1, le=8000)
    parent_message_id: UUID | None = None

