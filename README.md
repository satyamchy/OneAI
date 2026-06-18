# PAIOS

PAIOS is a Personal AI Operating System. Phase 1 is the Chat Core: authentication, conversations, OpenRouter-powered streaming, mode-specific processing, run details, and persistent PostgreSQL storage.

## Services

- `backend`: FastAPI, async SQLAlchemy, PostgreSQL, Redis, OpenRouter, LangChain helpers.
- `frontend`: React, Vite, Tailwind CSS, React Router, Axios, markdown rendering.
- `postgres`: PostgreSQL 16 for persistent app data.
- `redis`: Redis 7 for rate limiting now and queues later.

## Local Setup Later

This scaffold intentionally does not install packages. Use these docs when you are ready:

- Backend setup: `docs/backend.md`
- Frontend setup: `docs/frontend.md`
- Architecture: `docs/architecture.md`
- API reference: `docs/api.md`
- Database notes: `docs/database.md`

## First Run Later

1. Copy `.env.example` to `.env` and fill `OPENROUTER_API_KEY` and `JWT_SECRET_KEY`.
2. Install backend packages from `backend/requirements.txt`.
3. Install frontend packages from `frontend/package.json`.
4. Run migrations with Alembic.
5. Start with Docker Compose or separate backend/frontend processes.

Proposed Folder Tree

paios/
├── backend/                         # FastAPI backend service
│   ├── app/                         # Main Python application package
│   │   ├── main.py                  # FastAPI app creation, middleware, and router mounting
│   │   ├── config.py                # Environment-driven settings loaded from .env
│   │   ├── database.py              # Async SQLAlchemy engine, session, and base model setup
│   │   ├── api/                     # HTTP API route modules
│   │   │   └── v1/                  # Versioned API routes mounted under /v1
│   │   │       ├── auth.py          # Register, login, and current-user endpoints
│   │   │       ├── conversations.py # Conversation CRUD and interaction-mode updates
│   │   │       ├── messages.py      # Message CRUD and streaming chat endpoint
│   │   │       └── models.py        # Model registry listing endpoints
│   │   ├── models/                  # SQLAlchemy database models
│   │   ├── schemas/                 # Pydantic v2 request and response schemas
│   │   ├── services/                # Business logic layer used by API routes
│   │   ├── providers/               # AI provider abstraction and OpenRouter implementation
│   │   ├── chains/                  # LangChain prompt/message formatting helpers
│   │   ├── tools/                   # Tool registry, executor, and tool implementations
│   │   ├── search/                  # Web search providers and search prompt formatting
│   │   ├── core/                    # Auth, dependencies, context building, constants, errors
│   │   ├── db/                      # Seed scripts and migration-related app helpers
│   │   └── utils/                   # Request IDs, token counting, and pricing helpers
│   ├── alembic/                     # Alembic migration environment
│   ├── requirements.txt             # Backend Python dependencies
│   └── Dockerfile                   # Backend development container
├── frontend/                        # React + Vite frontend service
│   ├── src/                         # Main React source code
│   │   ├── api/                     # Axios client and API wrapper functions
│   │   ├── pages/                   # Route-level pages: login, register, chat
│   │   ├── components/              # Small reusable UI components
│   │   ├── hooks/                   # React hooks such as useAuth
│   │   ├── store/                   # Client state management modules
│   │   ├── routes/                  # React Router route definitions and guards
│   │   └── utils/                   # Frontend helper functions
│   └── Dockerfile                   # Frontend development container
├── docs/                            # Project documentation
│   ├── architecture.md              # System architecture and mode pipeline notes
│   ├── api.md                       # API endpoint documentation
│   └── database.md                  # Database schema documentation
├── app/                             # Future top-level PAIOS modules outside Phase 1
│   ├── memory/                      # Future long-term memory system
│   ├── rag/                         # Future retrieval-augmented generation system
│   ├── agents/                      # Future autonomous agent workflows
│   └── integrations/                # Future Gmail, Slack, Notion, and other integrations
├── docker-compose.yml               # Local dev stack: postgres, redis, backend, frontend
├── .env.example                     # Example environment variables with no secrets
└── README.md                        # Local setup and project overview