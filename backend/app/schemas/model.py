from uuid import UUID
from pydantic import BaseModel

class ModelRead(BaseModel):
    id: UUID
    name: str
    provider: str
    context_window: int
    cost_per_input_token: float
    cost_per_output_token: float
    is_active: bool

    model_config = {"from_attributes": True}

class ModelListResponse(BaseModel):
    request_id: str
    models: list[ModelRead]
