from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import InteractionMode
from app.services.message_service import get_recent_messages

# Builds mode-specific conversation context before a prompt is sent to the model.
async def build_context(conversation_id, user_id, mode: InteractionMode, db: AsyncSession):
    if mode == InteractionMode.WEB_SEARCH:
        return []
    if mode == InteractionMode.CHAT:
        messages = await get_recent_messages(conversation_id, limit=20, db=db)
        # TODO Phase 2: inject long-term memories from memory_service.
        # TODO Phase 3: inject RAG chunks from rag_service.
        return messages
    if mode == InteractionMode.TOOLS:
        messages = await get_recent_messages(conversation_id, limit=10, db=db)
        # TODO Phase 5: inject agent memory and tool history.
        return messages
    return []
