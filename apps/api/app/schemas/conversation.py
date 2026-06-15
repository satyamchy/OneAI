from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ConversationCreate(BaseModel):
    title: str | None = Field(default="New Conversation", max_length=240)
    default_model_id: str | None = Field(default=None, max_length=160)
    settings_json: dict | None = None


class ConversationUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=240)
    status: str | None = Field(default=None, max_length=32)
    default_model_id: str | None = Field(default=None, max_length=160)
    settings_json: dict | None = None


class ConversationRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    status: str
    default_model_id: str | None
    settings_json: dict
    summary: str | None
    created_at: datetime
    updated_at: datetime

