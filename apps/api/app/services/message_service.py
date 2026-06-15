from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import not_found
from app.db.models.message import Message
from app.db.models.user import User
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)

    async def list_for_conversation(self, conversation_id: str, user: User) -> list[Message]:
        conversation = await self.conversations.get_owned(conversation_id, user.id)
        if not conversation:
            raise not_found("Conversation not found")
        return await self.messages.list_for_conversation(conversation.id)

