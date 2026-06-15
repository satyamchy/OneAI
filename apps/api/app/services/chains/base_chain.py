from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.services.providers.base_provider import ProviderChunk, ProviderRequest


class BaseChain(ABC):
    @abstractmethod
    async def stream(self, request: ProviderRequest) -> AsyncIterator[ProviderChunk]:
        raise NotImplementedError

