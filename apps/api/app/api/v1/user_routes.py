from fastapi import APIRouter

from app.core.dependencies import CurrentUser
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def me(user: CurrentUser) -> UserRead:
    return UserRead.model_validate(user)

