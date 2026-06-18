from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.run import ModelRunResponse
from app.services.run_service import get_model_run
from app.utils.request_id import generate_request_id

router = APIRouter(prefix="/model-runs", tags=["model-runs"])

# Returns full run metadata for a model run owned by the authenticated user.
@router.get("/{run_id}", response_model=ModelRunResponse)
async def read_model_run(run_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    run = await get_model_run(db, user, run_id)
    return ModelRunResponse(request_id=generate_request_id(), run=run)
