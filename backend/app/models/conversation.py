import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import InteractionMode
from app.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    # Primary unique identifier for the conversation.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # User who owns this conversation.
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    # Human-readable title, generated after the first message.
    title: Mapped[str] = mapped_column(String(255), default="New Conversation", nullable=False)
    # Default model selected for this conversation.
    selected_model: Mapped[str] = mapped_column(String(255), nullable=False)
    # Current interaction mode used by the next message unless overridden.
    interaction_mode: Mapped[InteractionMode] = mapped_column(Enum(InteractionMode), default=InteractionMode.CHAT, nullable=False)
    # Timestamp when the conversation was created.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # Timestamp when the conversation was last updated.
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    # Soft archive flag for hiding conversations without deleting data.
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
