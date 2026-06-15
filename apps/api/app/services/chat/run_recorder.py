import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.model_run import ModelRun
from app.db.repositories.model_run_repository import ModelRunRepository


class RunRecorder:
    def __init__(self, db: AsyncSession):
        self.runs = ModelRunRepository(db)

    async def start(
        self,
        *,
        request_id: str,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        request_message_id: uuid.UUID,
        provider: str,
        model_id: str,
    ) -> ModelRun:
        return await self.runs.create(
            request_id=request_id,
            user_id=user_id,
            conversation_id=conversation_id,
            request_message_id=request_message_id,
            provider=provider,
            model_id=model_id,
            status="started",
        )

    async def complete(
        self,
        run: ModelRun,
        *,
        response_message_id: uuid.UUID,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        estimated_cost_usd: float,
        latency_ms: int,
        provider: str,
        model_id: str,
        fallback_used: bool,
        fallback_from_model_id: str | None,
    ) -> ModelRun:
        return await self.runs.update(
            run,
            response_message_id=response_message_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            latency_ms=latency_ms,
            provider=provider,
            model_id=model_id,
            fallback_used=fallback_used,
            fallback_from_model_id=fallback_from_model_id,
            status="completed",
        )

    async def fail(self, run: ModelRun, *, error: Exception, latency_ms: int) -> ModelRun:
        return await self.runs.update(
            run,
            status="failed",
            latency_ms=latency_ms,
            error_code=error.__class__.__name__,
            error_message=str(error),
        )

