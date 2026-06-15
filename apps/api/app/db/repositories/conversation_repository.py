import uuid

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.conversation import Conversation
from app.db.models.message import Message


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _owned_query(self, user_id: uuid.UUID) -> Select[tuple[Conversation]]:
        return select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.status != "deleted",
        )

    async def list_for_user(self, user_id: uuid.UUID) -> list[Conversation]:
        result = await self.db.execute(
            self._owned_query(user_id).order_by(Conversation.updated_at.desc())
        )
        return list(result.scalars().all())

    async def get_owned(self, conversation_id: str | uuid.UUID, user_id: uuid.UUID) -> Conversation | None:
        result = await self.db.execute(
            self._owned_query(user_id).where(Conversation.id == uuid.UUID(str(conversation_id)))
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        title: str,
        default_model_id: str | None,
        settings_json: dict | None = None,
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title,
            default_model_id=default_model_id,
            settings_json=settings_json or {},
        )
        self.db.add(conversation)
        await self.db.flush()
        return conversation

    async def update(self, conversation: Conversation, **values) -> Conversation:
        for key, value in values.items():
            if value is not None:
                setattr(conversation, key, value)
        await self.db.flush()
        return conversation

    async def soft_delete(self, conversation: Conversation) -> Conversation:
        conversation.status = "deleted"
        await self.db.flush()
        return conversation

    async def message_count(self, conversation_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Message.id)).where(Message.conversation_id == conversation_id)
        )
        return int(result.scalar_one())

