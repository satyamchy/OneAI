import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_for_conversation(self, conversation_id: str | uuid.UUID) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == uuid.UUID(str(conversation_id)))
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    async def recent_for_conversation(
        self,
        conversation_id: uuid.UUID,
        limit: int = 24,
    ) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))

    async def create(
        self,
        *,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        content: str,
        content_json: dict | None = None,
        model_id: str | None = None,
        provider: str | None = None,
        model_run_id: uuid.UUID | None = None,
        parent_message_id: uuid.UUID | None = None,
        metadata_json: dict | None = None,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            content_json=content_json,
            model_id=model_id,
            provider=provider,
            model_run_id=model_run_id,
            parent_message_id=parent_message_id,
            metadata_json=metadata_json or {},
        )
        self.db.add(message)
        await self.db.flush()
        return message

    async def attach_model_run(self, message: Message, model_run_id: uuid.UUID) -> Message:
        message.model_run_id = model_run_id
        await self.db.flush()
        return message

