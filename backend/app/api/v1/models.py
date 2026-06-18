from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.models.model_registry import ModelRegistry
from app.models.user import User
from app.schemas.model import ModelListResponse
from app.utils.request_id import generate_request_id

router = APIRouter(prefix="/models", tags=["models"])

# Lists active chat models available to the UI.
@router.get("", response_model=ModelListResponse)
async def list_models(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(ModelRegistry).where(ModelRegistry.is_active.is_(True)).order_by(ModelRegistry.name.asc()))
    return ModelListResponse(request_id=generate_request_id(), models=list(result.scalars().all()))
