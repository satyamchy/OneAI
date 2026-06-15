from app.services.providers.base_provider import ModelProvider
from app.services.providers.openrouter_provider import OpenRouterProvider


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, ModelProvider] = {
            OpenRouterProvider.provider_name: OpenRouterProvider(),
        }

    def get(self, provider_name: str) -> ModelProvider:
        provider = self._providers.get(provider_name)
        if not provider:
            raise ValueError(f"Provider is not registered: {provider_name}")
        return provider

