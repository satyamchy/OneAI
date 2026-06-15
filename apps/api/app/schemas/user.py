from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.schemas.common import ORMModel


class UserRead(ORMModel):
    id: UUID
    email: EmailStr
    display_name: str | None
    default_model_id: str | None
    created_at: datetime
    updated_at: datetime

