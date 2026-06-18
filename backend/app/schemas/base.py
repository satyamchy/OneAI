from pydantic import BaseModel, ConfigDict

class APIResponse(BaseModel):
    request_id: str
