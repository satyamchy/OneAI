from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.analytics = AnalyticsRepository(db)

    async def usage_summary(self, user: User) -> dict:
        return await self.analytics.usage_summary(user_id=user.id)

