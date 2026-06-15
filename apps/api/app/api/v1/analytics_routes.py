from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.analytics import UsageSummary
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/usage", response_model=UsageSummary)
async def usage_summary(db: DbSession, user: CurrentUser) -> UsageSummary:
    return UsageSummary.model_validate(await AnalyticsService(db).usage_summary(user))

