from pydantic import BaseModel


class UsageSummary(BaseModel):
    runs: int
    tokens: int
    estimated_cost_usd: float
    avg_latency_ms: int

