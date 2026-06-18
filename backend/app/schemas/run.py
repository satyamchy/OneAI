from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.core.constants import RunStatus

class ModelRunRead(BaseModel):
    id: UUID
    message_id: UUID
    model_requested: str
    model_used: str
    provider: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    estimated_cost: float
    status: RunStatus
    fallback_reason: str | None = None
    request_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ModelRunResponse(BaseModel):
    request_id: str
    run: ModelRunRead
