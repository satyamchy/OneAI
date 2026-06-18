import json
from collections.abc import AsyncIterator
import httpx
from app.config import settings
from app.providers.base import ChatProvider

class OpenRouterProvider(ChatProvider):
    def __init__(self):
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

    # Streams assistant content deltas from OpenRouter's OpenAI-compatible endpoint.
    async def stream_chat(self, messages: list[dict], model: str, tools: list[dict] | None = None) -> AsyncIterator[str]:
        payload = {"model": model, "messages": messages, "stream": True}
        if tools:
            payload["tools"] = tools
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}/chat/completions", headers=self.headers, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line.removeprefix("data: ").strip()
                    if data == "[DONE]":
                        break
                    event = json.loads(data)
                    delta = event.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content")
                    if content:
                        yield content

    # Performs a non-streaming completion and returns the raw provider JSON.
    async def complete_chat(self, messages: list[dict], model: str, tools: list[dict] | None = None) -> dict:
        payload = {"model": model, "messages": messages}
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
