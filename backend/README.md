# PAIOS Backend

FastAPI backend for Phase 1 Chat Core: auth, conversations, messages, OpenRouter streaming, DuckDuckGo web search, tools, and run metadata.

## Install Later

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure Later

Copy the root `.env.example` to `.env` and set:

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`
- `OPENROUTER_API_KEY`

## Run Later

```bash
alembic upgrade head
python -m app.db.seed_models
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Structure

- `app/api/v1`: versioned HTTP routes.
- `app/models`: SQLAlchemy async declarative models.
- `app/schemas`: Pydantic v2 request and response schemas.
- `app/services`: business logic and streaming orchestration.
- `app/providers`: model provider abstraction and OpenRouter implementation.
- `app/search`: DuckDuckGo search and source prompt builder.
- `app/tools`: tool registry, executor, and implementations.
- `app/core`: auth, dependencies, context builder, constants, exceptions.
- `app/db`: seed scripts and migration helpers.
