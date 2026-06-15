from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.db.repositories.model_repository import ModelRepository
from app.schemas.model import ModelRead
from app.seeds.model_registry import DEFAULT_MODELS

router = APIRouter()


@router.get("", response_model=list[ModelRead])
async def list_models(db: DbSession, user: CurrentUser) -> list[ModelRead]:
    repository = ModelRepository(db)
    models = await repository.list_active()
    if not models:
        await repository.upsert_many(DEFAULT_MODELS)
        await db.commit()
        models = await repository.list_active()
    return [ModelRead.model_validate(model) for model in models]

