from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.core.exceptions import not_found
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationUpdate

# Creates a new conversation owned by the current user.
async def create_conversation(db: AsyncSession, user: User, payload: ConversationCreate) -> Conversation:
    conversation = Conversation(
        user_id=user.id,
        title=payload.title or "New Conversation",
        selected_model=payload.selected_model or settings.openrouter_default_model,
        interaction_mode=payload.interaction_mode,
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation

# Lists non-archived conversations owned by the current user.
async def list_conversations(db: AsyncSession, user: User) -> list[Conversation]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id, Conversation.is_archived.is_(False))
        .order_by(Conversation.updated_at.desc())
    )
    return list(result.scalars().all())

# Fetches one conversation by ID and verifies ownership.
async def get_conversation(db: AsyncSession, user: User, conversation_id: UUID) -> Conversation:
    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user.id))
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise not_found("Conversation not found")
    return conversation

# Applies partial updates to a conversation owned by the current user.
async def update_conversation(db: AsyncSession, user: User, conversation_id: UUID, payload: ConversationUpdate) -> Conversation:
    conversation = await get_conversation(db, user, conversation_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(conversation, field, value)
    await db.commit()
    await db.refresh(conversation)
    return conversation

# Deletes a conversation owned by the current user.
async def delete_conversation(db: AsyncSession, user: User, conversation_id: UUID) -> None:
    conversation = await get_conversation(db, user, conversation_id)
    await db.delete(conversation)
    await db.commit()
