from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.conversation import Conversation
from app.db.repositories.message_repository import MessageRepository
from app.services.providers.base_provider import ProviderMessage


class ContextBuilder:
    def __init__(self, db: AsyncSession):
        self.messages = MessageRepository(db)

    async def build(self, conversation: Conversation) -> list[ProviderMessage]:
        recent_messages = await self.messages.recent_for_conversation(conversation.id, limit=24)
        return [
            ProviderMessage(role=message.role, content=message.content)
            for message in recent_messages
            if message.role in {"user", "assistant", "system"}
        ]

