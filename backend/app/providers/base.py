from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

class ChatProvider(ABC):
    # Streams assistant response text from the configured provider.
    @abstractmethod
    async def stream_chat(self, messages: list[dict], model: str, tools: list[dict] | None = None) -> AsyncIterator[str]:
        raise NotImplementedError

    # Sends a non-streaming chat request, useful for tool-call planning.
    @abstractmethod
    async def complete_chat(self, messages: list[dict], model: str, tools: list[dict] | None = None) -> dict:
        raise NotImplementedError
