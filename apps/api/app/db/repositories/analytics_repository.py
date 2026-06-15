import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analytics_event import AnalyticsEvent
from app.db.models.model_run import ModelRun


class AnalyticsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(
        self,
        *,
        user_id: uuid.UUID | None,
        conversation_id: uuid.UUID | None,
        event_name: str,
        event_props_json: dict | None = None,
    ) -> AnalyticsEvent:
        event = AnalyticsEvent(
            user_id=user_id,
            conversation_id=conversation_id,
            event_name=event_name,
            event_props_json=event_props_json or {},
        )
        self.db.add(event)
        await self.db.flush()
        return event

    async def usage_summary(
        self,
        *,
        user_id: uuid.UUID,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> dict:
        query = select(
            func.count(ModelRun.id),
            func.coalesce(func.sum(ModelRun.total_tokens), 0),
            func.coalesce(func.sum(ModelRun.estimated_cost_usd), 0),
            func.coalesce(func.avg(ModelRun.latency_ms), 0),
        ).where(ModelRun.user_id == user_id)
        if start:
            query = query.where(ModelRun.created_at >= start)
        if end:
            query = query.where(ModelRun.created_at <= end)

        runs, tokens, cost, avg_latency = (await self.db.execute(query)).one()
        return {
            "runs": runs,
            "tokens": tokens,
            "estimated_cost_usd": float(cost or 0),
            "avg_latency_ms": int(avg_latency or 0),
        }

