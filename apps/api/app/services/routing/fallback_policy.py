from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.model_registry import ModelRegistry
from app.db.repositories.model_repository import ModelRepository
from app.services.routing.model_router import SelectedModel


class FallbackPolicy:
    def __init__(self, db: AsyncSession):
        self.models = ModelRepository(db)

    async def resolve(self, current: ModelRegistry) -> SelectedModel | None:
        fallback_model_id = current.fallback_model_id or settings.fallback_model_id
        if not fallback_model_id or fallback_model_id == current.model_id:
            return None

        fallback = await self.models.get_by_model_id(fallback_model_id)
        if not fallback:
            return None

        return SelectedModel(
            provider=fallback.provider,
            model_id=fallback.model_id,
            registry_model=fallback,
        )

