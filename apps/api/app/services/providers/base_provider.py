from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class ProviderMessage:
    role: str
    content: str


@dataclass(slots=True)
class ProviderRequest:
    model_id: str
    messages: list[ProviderMessage]
    request_id: str
    temperature: float = 0.7
    max_tokens: int = 1200


@dataclass(slots=True)
class ProviderChunk:
    content: str = ""
    finish_reason: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0


class ModelProvider(Protocol):
    provider_name: str

    async def stream_chat(self, request: ProviderRequest) -> AsyncIterator[ProviderChunk]:
        ...

    async def complete(self, request: ProviderRequest) -> str:
        ...

    async def health_check(self) -> bool:
        ...

