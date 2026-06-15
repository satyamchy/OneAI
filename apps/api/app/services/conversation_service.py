from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import not_found
from app.db.models.conversation import Conversation
from app.db.models.user import User
from app.db.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationCreate, ConversationUpdate


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversations = ConversationRepository(db)

    async def list_for_user(self, user: User) -> list[Conversation]:
        return await self.conversations.list_for_user(user.id)

    async def get_owned(self, conversation_id: str, user: User) -> Conversation:
        conversation = await self.conversations.get_owned(conversation_id, user.id)
        if not conversation:
            raise not_found("Conversation not found")
        return conversation

    async def create(self, payload: ConversationCreate, user: User) -> Conversation:
        conversation = await self.conversations.create(
            user_id=user.id,
            title=payload.title or "New Conversation",
            default_model_id=payload.default_model_id or user.default_model_id or settings.default_model_id,
            settings_json=payload.settings_json or {},
        )
        await self.db.commit()
        return conversation

    async def update(
        self,
        conversation_id: str,
        payload: ConversationUpdate,
        user: User,
    ) -> Conversation:
        conversation = await self.get_owned(conversation_id, user)
        values = payload.model_dump(exclude_unset=True)
        await self.conversations.update(conversation, **values)
        await self.db.commit()
        return conversation

    async def delete(self, conversation_id: str, user: User) -> None:
        conversation = await self.get_owned(conversation_id, user)
        await self.conversations.soft_delete(conversation)
        await self.db.commit()

