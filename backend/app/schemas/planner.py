from typing import Literal, Any

from pydantic import BaseModel, Field


class ToolStep(BaseModel):

    tool: Literal[
        "web_search",
        "calculator"
    ]

    input: dict[str, Any] = Field(default_factory=dict)


class PlannerResponse(BaseModel):

    steps: list[ToolStep] = Field(default_factory=list)

    is_finished: bool

    reason: str = ""