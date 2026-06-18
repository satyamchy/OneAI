import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import InteractionMode, MessageRole
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    # Primary unique identifier for the message.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Conversation this message belongs to.
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=False)
    # Role of the message author.
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    # Raw text content of the message.
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # Actual model that generated this assistant message.
    model_used: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Interaction mode used when this message was created.
    mode_used: Mapped[InteractionMode | None] = mapped_column(Enum(InteractionMode), nullable=True)
    # Raw tool call request and result for tools mode.
    tool_calls_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # Raw web search sources for web search mode.
    search_sources_json: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    # Timestamp when the message was created.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    model_run = relationship("ModelRun", back_populates="message", uselist=False, cascade="all, delete-orphan")
