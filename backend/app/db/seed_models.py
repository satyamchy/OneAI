import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.model_registry import ModelRegistry

DEFAULT_MODELS = [
    {"name": "openai/gpt-4o-mini", "provider": "openrouter", "context_window": 128000},
    {"name": "anthropic/claude-3.5-sonnet", "provider": "openrouter", "context_window": 200000},
    {"name": "google/gemini-flash-1.5", "provider": "openrouter", "context_window": 1000000},
    {"name": "meta-llama/llama-3.1-70b-instruct", "provider": "openrouter", "context_window": 131000},
]

# Seeds the local model registry with useful OpenRouter model defaults.
async def seed_models() -> None:
    async with AsyncSessionLocal() as db:
        for item in DEFAULT_MODELS:
            existing = await db.execute(select(ModelRegistry).where(ModelRegistry.name == item["name"]))
            if not existing.scalar_one_or_none():
                db.add(ModelRegistry(**item))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed_models())
