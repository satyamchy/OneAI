import asyncio
import json
from collections.abc import AsyncIterator

import httpx

from app.core.config import settings
from app.services.providers.base_provider import ProviderChunk, ProviderMessage, ProviderRequest


class OpenRouterProvider:
    provider_name = "openrouter"

    async def stream_chat(self, request: ProviderRequest) -> AsyncIterator[ProviderChunk]:
        if not settings.openrouter_api_key and settings.mock_model_when_missing_key:
            async for chunk in self._mock_stream(request):
                yield chunk
            return

        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")

        payload = {
            "model": request.model_id,
            "messages": [self._message_to_dict(message) for message in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

        url = f"{settings.openrouter_base_url.rstrip('/')}/chat/completions"
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data = line.removeprefix("data:").strip()
                    if data == "[DONE]":
                        break
                    try:
                        event = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choice = (event.get("choices") or [{}])[0]
                    delta = choice.get("delta") or {}
                    content = delta.get("content") or ""
                    finish_reason = choice.get("finish_reason")
                    if content or finish_reason:
                        yield ProviderChunk(content=content, finish_reason=finish_reason)

    async def complete(self, request: ProviderRequest) -> str:
        chunks: list[str] = []
        async for chunk in self.stream_chat(request):
            chunks.append(chunk.content)
        return "".join(chunks)

    async def health_check(self) -> bool:
        return bool(settings.openrouter_api_key) or settings.mock_model_when_missing_key

    def _message_to_dict(self, message: ProviderMessage) -> dict[str, str]:
        return {"role": message.role, "content": message.content}

    async def _mock_stream(self, request: ProviderRequest) -> AsyncIterator[ProviderChunk]:
        latest_user = next(
            (message.content for message in reversed(request.messages) if message.role == "user"),
            "your prompt",
        )
        text = (
            "This is a local mock response because OPENROUTER_API_KEY is not configured. "
            f"I received: {latest_user[:180]}. "
            "The full OpenRouter provider path is wired, so adding the key will switch this "
            "same chain to live model streaming."
        )
        for word in text.split(" "):
            await asyncio.sleep(0.015)
            yield ProviderChunk(content=f"{word} ")

