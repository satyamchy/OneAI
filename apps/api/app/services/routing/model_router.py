from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.conversation import Conversation
from app.db.models.model_registry import ModelRegistry
from app.db.models.user import User
from app.db.repositories.model_repository import ModelRepository
from app.seeds.model_registry import DEFAULT_MODELS


@dataclass(slots=True)
class SelectedModel:
    provider: str
    model_id: str
    registry_model: ModelRegistry


class ModelRouter:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.models = ModelRepository(db)

    async def select_model(
        self,
        *,
        user: User,
        conversation: Conversation,
        requested_model_id: str | None,
    ) -> SelectedModel:
        candidates = [
            requested_model_id,
            conversation.default_model_id,
            user.default_model_id,
            settings.default_model_id,
        ]
        for model_id in candidates:
            if not model_id:
                continue
            model = await self.models.get_by_model_id(model_id)
            if model:
                return SelectedModel(
                    provider=model.provider,
                    model_id=model.model_id,
                    registry_model=model,
                )

        fallback = await self.models.first_active()
        if not fallback:
            await self.models.upsert_many(DEFAULT_MODELS)
            await self.db.flush()
            fallback = await self.models.first_active()
        if not fallback:
            raise RuntimeError("No active models are configured")
        return SelectedModel(
            provider=fallback.provider,
            model_id=fallback.model_id,
            registry_model=fallback,
        )
