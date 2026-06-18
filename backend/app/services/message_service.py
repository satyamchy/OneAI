from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import InteractionMode, MessageRole
from app.models.message import Message

# Persists a message for a conversation.
async def create_message(db: AsyncSession, conversation_id: UUID, role: MessageRole, content: str, model_used: str | None = None, mode_used: InteractionMode | None = None, tool_calls_json=None, search_sources_json=None) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        model_used=model_used,
        mode_used=mode_used,
        tool_calls_json=tool_calls_json,
        search_sources_json=search_sources_json,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

# Lists messages for a conversation from oldest to newest.
async def list_messages(db: AsyncSession, conversation_id: UUID) -> list[Message]:
    result = await db.execute(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()))
    return list(result.scalars().all())

# Gets recent messages for prompt context while preserving chronological order.
async def get_recent_messages(conversation_id: UUID, limit: int, db: AsyncSession) -> list[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    return list(reversed(result.scalars().all()))
