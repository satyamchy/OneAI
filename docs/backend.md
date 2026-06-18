# Backend Setup Notes

This backend is FastAPI with async SQLAlchemy, PostgreSQL, Redis, JWT auth, LangChain helpers, and OpenRouter via `httpx`.

## Install Later

From `paios/backend`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Later

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Migrations Later

Alembic tracks database schema changes as versioned migration files. The first migration creates users, conversations, messages, model registry, and model runs.

```bash
alembic upgrade head
python -m app.db.seed_models
```

## Backend Structure

- `app/api/v1`: HTTP routes under `/v1`.
- `app/models`: SQLAlchemy tables.
- `app/schemas`: Pydantic request and response contracts.
- `app/services`: business logic and streaming orchestration.
- `app/providers`: OpenRouter provider abstraction.
- `app/tools`: OpenAI-compatible tool definitions and executors.
- `app/search`: DuckDuckGo web search and prompt building.
- `app/core`: auth, dependencies, constants, context builder.
