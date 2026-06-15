from datetime import datetime
from uuid import UUID

from app.schemas.common import ORMModel


class ModelRead(ORMModel):
    id: UUID
    provider: str
    model_id: str
    display_name: str
    capabilities_json: dict
    context_window: int
    supports_streaming: bool
    supports_tools: bool
    input_cost_per_1m: float
    output_cost_per_1m: float
    fallback_model_id: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

