from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import RunStatus
from app.core.exceptions import not_found
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.model_run import ModelRun
from app.utils.pricing import estimate_cost

# Records metadata about a completed or failed model call.
async def record_model_run(db: AsyncSession, message_id: UUID, model_requested: str, model_used: str, provider: str, input_tokens: int, output_tokens: int, latency_ms: int, request_id: str, status: RunStatus = RunStatus.SUCCESS, fallback_reason: str | None = None) -> ModelRun:
    run = ModelRun(
        message_id=message_id,
        model_requested=model_requested,
        model_used=model_used,
        provider=provider,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        estimated_cost=estimate_cost(input_tokens, output_tokens),
        status=status,
        fallback_reason=fallback_reason,
        request_id=request_id,
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run


# Fetches one model run and verifies it belongs to the authenticated user.
async def get_model_run(db: AsyncSession, user, run_id: UUID) -> ModelRun:
    result = await db.execute(
        select(ModelRun)
        .join(Message, ModelRun.message_id == Message.id)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .where(ModelRun.id == run_id, Conversation.user_id == user.id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise not_found("Model run not found")
    return run
