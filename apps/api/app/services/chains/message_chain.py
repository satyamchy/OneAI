from collections.abc import AsyncIterator

from app.services.chains.base_chain import BaseChain
from app.services.providers.base_provider import ProviderChunk, ProviderRequest
from app.services.providers.provider_registry import ProviderRegistry


class MessageChain(BaseChain):
    def __init__(self, provider_registry: ProviderRegistry, provider_name: str):
        self.provider = provider_registry.get(provider_name)

    async def stream(self, request: ProviderRequest) -> AsyncIterator[ProviderChunk]:
        async for chunk in self.provider.stream_chat(request):
            yield chunk

