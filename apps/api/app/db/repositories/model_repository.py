from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.model_registry import ModelRegistry


class ModelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_active(self) -> list[ModelRegistry]:
        result = await self.db.execute(
            select(ModelRegistry)
            .where(ModelRegistry.is_active.is_(True))
            .order_by(ModelRegistry.display_name.asc())
        )
        return list(result.scalars().all())

    async def get_by_model_id(self, model_id: str) -> ModelRegistry | None:
        result = await self.db.execute(
            select(ModelRegistry).where(
                ModelRegistry.model_id == model_id,
                ModelRegistry.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def first_active(self) -> ModelRegistry | None:
        result = await self.db.execute(
            select(ModelRegistry)
            .where(ModelRegistry.is_active.is_(True))
            .order_by(ModelRegistry.display_name.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def upsert_many(self, models: list[dict]) -> None:
        for model in models:
            stmt = insert(ModelRegistry).values(**model)
            stmt = stmt.on_conflict_do_update(
                index_elements=[ModelRegistry.model_id],
                set_={
                    "provider": stmt.excluded.provider,
                    "display_name": stmt.excluded.display_name,
                    "capabilities_json": stmt.excluded.capabilities_json,
                    "context_window": stmt.excluded.context_window,
                    "supports_streaming": stmt.excluded.supports_streaming,
                    "supports_tools": stmt.excluded.supports_tools,
                    "input_cost_per_1m": stmt.excluded.input_cost_per_1m,
                    "output_cost_per_1m": stmt.excluded.output_cost_per_1m,
                    "fallback_model_id": stmt.excluded.fallback_model_id,
                    "is_active": stmt.excluded.is_active,
                },
            )
            await self.db.execute(stmt)

