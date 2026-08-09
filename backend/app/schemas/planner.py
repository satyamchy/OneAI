from typing import Literal, Any

from pydantic import BaseModel, Field


# class ToolStep(BaseModel):
#     tool: Literal[
#         "web_search",
#         "calculator"
#     ]
#     input: dict[str, Any] = Field(default_factory=dict, 
#              description="The exact search query or input required by the selected tool"
#         )
class ToolStep(BaseModel):
    tool: Literal[
        "web_search",
        "calculator"
    ]

    input: dict[str, Any] = Field(
        description=(
            "Arguments for the selected tool. "
            "For web_search, use {'query': '<search query>'}. "
            "For calculator, use {'expression': '<mathematical expression>'}. "
            "Never return an empty object."
        )
    )

class PlannerResponse(BaseModel):

    steps: list[ToolStep] = Field(default_factory=list)

    is_finished: bool

    reason: str = ""