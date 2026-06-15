import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.model_run import ModelRun


class ModelRunRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        request_id: str,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        request_message_id: uuid.UUID | None,
        provider: str,
        model_id: str,
        status: str = "started",
        fallback_used: bool = False,
        fallback_from_model_id: str | None = None,
        metadata_json: dict | None = None,
    ) -> ModelRun:
        run = ModelRun(
            request_id=request_id,
            user_id=user_id,
            conversation_id=conversation_id,
            request_message_id=request_message_id,
            provider=provider,
            model_id=model_id,
            status=status,
            fallback_used=fallback_used,
            fallback_from_model_id=fallback_from_model_id,
            metadata_json=metadata_json or {},
        )
        self.db.add(run)
        await self.db.flush()
        return run

    async def update(self, run: ModelRun, **values) -> ModelRun:
        for key, value in values.items():
            setattr(run, key, value)
        await self.db.flush()
        return run

