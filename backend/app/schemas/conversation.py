from pydantic import BaseModel, Field
from typing import List


class Source(BaseModel):
    title: str = Field(default="Untitled source")
    url: str = Field(default="")
    snippet: str = Field(default="")


class RunResponse(BaseModel):
    query: str
    answer: str
    sources: List[Source] = []
    success: bool = True
    message: str = "ok"