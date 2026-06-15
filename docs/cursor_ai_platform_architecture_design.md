# AI platform architecture design
_Exported on 09/06/2026 at 15:54:35 GMT+5:30 from Cursor (3.4.20)_

---

**User**

You are a senior AI product architect, system designer, and full-stack staff engineer.

Design a production-grade AI platform for me with the following goals:

Core goals:
Multi-model support
Dynamic model selection by me at runtime
Long-term memory
Custom RAG
Business data support
Analytics
Future AI agents
User profiles
Integrations with Gmail, Slack, Notion, and similar external apps
Web search support when required

Important architecture preference:
The application must not be tied to a single model provider.
The memory, conversation history, and business data must be owned by my platform.
Models should be swappable dynamically.
The design should support OpenRouter as the model gateway, with GPT, Claude, Gemini, Groq, and DeepSeek as possible providers.

Preferred technology stack:
Frontend: React
Backend: FastAPI or Node.js/NestJS
Data layer: either PostgreSQL + pgvector, or an advanced architecture using S3 and a Snowflake-like data design where appropriate
Memory layer should include:
  - conversations
  - messages
  - user_memories
  - user profiles
  - embeddings
  - retrieved knowledge chunks
Redis may be used for caching, queues, and session handling

What I want you to produce:
1. A complete high-level design (HLD)
2. A system architecture diagram in text form
3. A functional requirements document
4. A non-functional requirements document
5. A detailed database design
6. A memory architecture design
7. A RAG architecture design
8. A model routing and fallback strategy
9. A web search integration strategy
10. A third-party app integration strategy
11. An analytics architecture
12. An API design outline
13. A security and access control design
14. A deployment and scaling plan
15. An MVP roadmap
16. A phase-wise build plan from MVP to full platform

For the memory system, include:
short-term chat context
long-term user preferences
durable user facts
semantic retrieval of older conversations
memory write rules
memory update rules
memory deletion rules
confidence or relevance scoring

For the RAG system, include:
document ingestion
chunking
embedding generation
indexing
retrieval
reranking
prompt assembly
citation/traceability strategy

For integrations, include:
Gmail
Slack
Notion
Google Drive
Calendar
future plugin/MCP-style connectors if suitable

For model routing, include:
provider abstraction
manual model selection
automatic fallback if one provider fails or rate limits
cost-aware routing
latency-aware routing
user override support

For the final output, be very practical:
Use clear sections
Use tables where useful
Include data flow
Include component responsibilities
Include example API endpoints
Include sample database tables
Include recommended folder structure
Include build order and development milestones

Also include:
Which parts should be built first
Which parts should be outsourced to existing tools or services
Which parts should remain custom-owned by my platform
Tradeoffs between PostgreSQL + pgvector versus S3 + Snowflake-like architecture for this use case

Knowledge Management & Notes System

The platform must include a first-class Knowledge & Notes Management system, similar to a combination of Notion, Obsidian, and ChatGPT.

Requirements:
Users can create, edit, organize, tag, search, and manage notes.
Notes can be created manually or generated automatically from AI conversations.
Users can save specific messages, conversation summaries, insights, code snippets, research findings, and learning materials into notes.
AI should be able to convert conversations into structured notes, summaries, study guides, flashcards, interview questions, revision sheets, and knowledge articles.
Notes must support folders, collections, tags, backlinks, and semantic search.
Notes should be indexed and embedded for retrieval through RAG.
Notes must be separate from AI memory. Memory is for AI personalization and context retrieval, while Notes are user-owned knowledge artifacts.
The system should support a personal knowledge base that grows over time from conversations, uploaded documents, web research, and external integrations.
Include database schema, APIs, retrieval architecture, note lifecycle, indexing strategy, and UX flows for the Notes system.

Design the platform as a Personal AI Operating System containing:
Chat
Memory
Notes
Knowledge Base
Documents
Integrations
Web Search
Analytics
Agents
Multi-Model Support

My preferred outcome is a design that feels like a personal AI operating system, where the UI, memory, integrations, and data are mine, while the underlying LLM can change anytime.

so please create a hld or architecture so that i can create it step by step with above methodology and as per my requirements

can you crate a pdf for the requiremtns with all the steps of how to build the project

---

**Cursor**

I'll explore the workspace for any existing project context, then produce a complete architecture document you can build from step by step.


# Personal AI Operating System — High-Level Design (HLD)

This is a production-grade architecture for a **provider-agnostic Personal AI OS** where you own the data, UI, memory, notes, and integrations — while LLMs remain swappable via OpenRouter (or direct providers).

> **Note on PDF:** I'm in **Ask mode** and cannot write files or generate a PDF. This document is complete and ready to save. To have me generate a `docs/PAIOS-Architecture.pdf` (or `.md` → PDF), switch to **Agent mode** and ask me to export it.

---

## 1. Executive Summary

| Principle | Decision |
|-----------|----------|
| **Data ownership** | All conversations, memory, notes, embeddings, and business data live in **your** PostgreSQL + object storage |
| **Model neutrality** | OpenRouter as primary gateway; direct provider adapters as fallback |
| **Separation of concerns** | **Memory** = AI personalization; **Notes** = user-owned knowledge artifacts |
| **Build strategy** | MVP on PostgreSQL + pgvector + Redis; evolve to lakehouse (S3 + warehouse) for analytics at scale |
| **Integration pattern** | OAuth connectors + MCP-style plugin runtime for future extensibility |

---

## 2. System Architecture Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER (React SPA)                              │
│  Chat │ Notes │ Knowledge Base │ Documents │ Integrations │ Settings │ Agents  │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │ HTTPS / WebSocket
┌───────────────────────────────────▼─────────────────────────────────────────────┐
│                         API GATEWAY (Kong / AWS ALB + FastAPI)                  │
│              Auth (JWT) │ Rate Limit │ Tenant Isolation │ Request Tracing         │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼────────┐        ┌─────────▼─────────┐       ┌────────▼────────┐
│  Chat Service  │        │  Notes Service    │       │ Integration Svc │
│  (orchestrator)│        │  (CRUD + graph)   │       │ (OAuth + sync)  │
└───────┬────────┘        └─────────┬─────────┘       └────────┬────────┘
        │                           │                           │
        │         ┌─────────────────┼─────────────────┐         │
        │         │                 │                 │         │
┌───────▼─────────▼──┐   ┌──────────▼──────────┐  ┌───▼─────────▼───┐
│   AI Orchestrator  │   │   RAG Pipeline      │  │  Connector Hub    │
│   (model router)   │   │ ingest/retrieve     │  │ Gmail/Slack/...   │
└───────┬────────────┘   └──────────┬──────────┘  └───┬─────────────┘
        │                             │                  │
┌───────▼────────────┐   ┌────────────▼──────────┐      │
│  Model Gateway     │   │  Embedding Service    │      │
│  (OpenRouter +     │   │  (batch + realtime)   │      │
│   direct adapters) │   └────────────┬──────────┘      │
└───────┬────────────┘                │                  │
        │                             │                  │
┌───────▼────────────┐   ┌────────────▼──────────┐  ┌───▼───────────────┐
│  Memory Service    │   │  Vector Index         │  │  Web Search Svc     │
│  STM + LTM + rules │   │  (pgvector → Qdrant)  │  │  Tavily/Serper/...  │
└───────┬────────────┘   └────────────┬──────────┘  └───────────────────┘
        │                             │
┌───────▼─────────────────────────────▼─────────────────────────────────────────┐
│                              DATA LAYER                                         │
│  PostgreSQL (OLTP) │ pgvector │ Redis (cache/queue/session) │ S3 (blobs/docs)  │
│  ────────────────────────────────────────────────────────────────────────────  │
│  Future: S3 data lake + Snowflake/BigQuery/DuckDB for analytics & batch RAG    │
└─────────────────────────────────────────────────────────────────────────────────┘
        │
┌───────▼─────────────────────────────────────────────────────────────────────────┐
│  ASYNC WORKERS (Celery / BullMQ)                                                │
│  doc ingestion │ embedding jobs │ memory extraction │ integration sync │ agents │
└─────────────────────────────────────────────────────────────────────────────────┘
        │
┌───────▼─────────────────────────────────────────────────────────────────────────┐
│  OBSERVABILITY: OpenTelemetry │ Prometheus │ Grafana │ structured logs            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Request Flow: Chat with Memory + RAG + Model Routing

```
User message
  → API Gateway (auth, rate limit)
  → Chat Service loads conversation + user profile
  → Memory Service: STM window + LTM retrieval (semantic)
  → RAG Service: retrieve from documents + notes (if enabled)
  → Optional: Web Search (if tool triggered or user setting)
  → Optional: Integration context (recent Gmail, Slack threads)
  → Prompt Assembler (system + memory + RAG + tools + user message)
  → Model Router (user-selected model or auto policy)
  → OpenRouter / direct provider (stream response)
  → Stream to client via WebSocket/SSE
  → Post-turn: persist message, extract memories, suggest note saves, log analytics
```

---

## 3. Functional Requirements Document (FRD)

### 3.1 Core Platform

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Users can authenticate and manage profiles | P0 |
| FR-02 | Multi-model chat with streaming responses | P0 |
| FR-03 | Runtime model selection per conversation or message | P0 |
| FR-04 | Conversation history persisted and searchable | P0 |
| FR-05 | Short-term context window management | P0 |
| FR-06 | Long-term memory extraction and retrieval | P0 |
| FR-07 | Document upload and custom RAG | P0 |
| FR-08 | Notes system (CRUD, tags, folders, backlinks) | P0 |
| FR-09 | Save messages/conversations to notes | P1 |
| FR-10 | AI-generated structured notes (summaries, flashcards, etc.) | P1 |
| FR-11 | Web search when required | P1 |
| FR-12 | Analytics dashboard (usage, cost, latency) | P1 |
| FR-13 | OAuth integrations (Gmail, Slack, Notion, Drive, Calendar) | P2 |
| FR-14 | AI agents with tool use | P2 |
| FR-15 | MCP-style plugin connectors | P3 |

### 3.2 Chat

- Create/rename/archive/delete conversations
- Branch conversations (fork from message)
- Attach documents to conversations
- Toggle RAG sources (documents, notes, web)
- Select model per chat or override per message
- Regenerate, edit, delete messages
- Export conversation

### 3.3 Memory (AI-owned personalization)

- Extract user preferences, facts, goals from conversations
- Semantic recall of older conversations
- Memory confidence scores and decay
- User can view, edit, pin, or delete memories
- **Explicit separation from Notes**

### 3.4 Notes (User-owned knowledge)

- Rich text / Markdown notes
- Folders, collections, tags, backlinks (wiki-style `[[links]]`)
- Full-text + semantic search
- Auto-save from chat (message, summary, insight)
- AI transforms: study guide, flashcards, interview Qs, revision sheet
- Version history
- Embeddings for RAG (notes are **retrieval sources**, not memory)

### 3.5 Documents & Knowledge Base

- Upload PDF, DOCX, TXT, MD, HTML
- Folder organization
- Chunking, embedding, indexing pipeline
- Citation in chat responses
- Re-index on update

### 3.6 Integrations

- OAuth 2.0 connect/disconnect
- Sync metadata (not full mirror initially)
- Query integration data as RAG/tool context
- Webhooks for Slack events (future)

### 3.7 Analytics

- Token usage per model/provider
- Cost tracking
- Latency percentiles
- Memory/RAG hit rates
- Integration sync health

---

## 4. Non-Functional Requirements (NFR)

| Category | Requirement | Target |
|----------|-------------|--------|
| **Availability** | Core chat API uptime | 99.9% |
| **Latency** | Time to first token (p95) | < 2s (excl. model) |
| **Latency** | RAG retrieval (p95) | < 300ms |
| **Scalability** | Concurrent users (MVP) | 100; scale to 10K+ |
| **Data residency** | User data in owned DB/S3 | Full control |
| **Security** | Encryption at rest + in transit | TLS 1.3, AES-256 |
| **Compliance** | GDPR delete/export | Right to erasure |
| **Observability** | Distributed tracing | 100% API requests traced |
| **Cost** | Model spend visibility | Per-user, per-model |
| **Portability** | Provider swap | < 1 day config change |
| **Testability** | Contract tests for model gateway | CI on every deploy |

---

## 5. Technology Stack Recommendation

| Layer | Recommendation | Rationale |
|-------|----------------|-----------|
| **Frontend** | React + TypeScript + Vite | Your preference; rich ecosystem |
| **UI** | Tailwind + shadcn/ui | Fast, consistent Personal OS feel |
| **State** | TanStack Query + Zustand | Server state + local UI state |
| **Backend** | **FastAPI (Python)** | Best for AI/ML pipelines, async, typing |
| **Workers** | Celery + Redis | Doc ingestion, embeddings, sync jobs |
| **OLTP DB** | PostgreSQL 16 + pgvector | Single store for MVP; you own everything |
| **Cache/Queue** | Redis 7 | Sessions, rate limits, job queues |
| **Object storage** | S3 / MinIO | Documents, exports, raw ingestion |
| **Vector (scale)** | pgvector → Qdrant (optional) | Start simple, migrate at ~10M vectors |
| **Model gateway** | OpenRouter + LiteLLM | Unified API, fallback, cost tracking |
| **Search** | Tavily or Serper + Brave fallback | Production web search APIs |
| **Auth** | Clerk or Auth0 (MVP) → custom later | Speed to market |
| **Analytics warehouse** | ClickHouse or DuckDB on S3 (Phase 3) | Cost-effective OLAP |

**Backend choice:** FastAPI over NestJS because Python dominates the AI ecosystem (LangChain/LlamaIndex optional, but you'll likely write custom orchestration).

---

## 6. PostgreSQL + pgvector vs S3 + Snowflake-like — Tradeoffs

| Dimension | PostgreSQL + pgvector | S3 + Warehouse (Snowflake-like) |
|-----------|----------------------|----------------------------------|
| **Best for** | MVP → mid-scale (< 50M vectors) | Analytics, batch RAG, multi-TB docs |
| **Latency** | Low (ms retrieval) | Higher (query spin-up) |
| **Ops complexity** | Low | High |
| **Cost at small scale** | Low ($50–200/mo) | High ($500+/mo minimum) |
| **Transactional integrity** | Excellent (ACID) | Eventual (ELT pipelines) |
| **Vector search** | Good up to ~10M vectors | Not native; needs external vector DB |
| **Your use case fit** | **Start here** | Add for analytics + cold archive |

### Recommended Hybrid Evolution

```
Phase 1: PostgreSQL + pgvector + S3 (hot path)
Phase 2: S3 data lake for raw docs + embedding parquet files
Phase 3: ClickHouse/DuckDB for analytics; Snowflake only if enterprise BI needed
Phase 4: Dedicated vector DB (Qdrant) if pgvector limits hit
```

**Rule:** Keep OLTP (users, chats, notes, memories) in PostgreSQL forever. Only offload **analytics** and **cold document archive** to lakehouse.

---

## 7. Detailed Database Design

### 7.1 Entity Relationship Overview

```
users ──┬── user_profiles
        ├── conversations ── messages
        ├── user_memories
        ├── notes ── note_links, note_tags, note_versions
        ├── documents ── document_chunks ── chunk_embeddings
        ├── integrations ── integration_tokens, sync_records
        ├── model_preferences
        └── analytics_events
```

### 7.2 Core Tables (Sample DDL)

```sql
-- USERS & PROFILES
CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  password_hash TEXT,  -- or external auth subject
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE user_profiles (
  user_id       UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  display_name  TEXT,
  timezone      TEXT DEFAULT 'UTC',
  locale        TEXT DEFAULT 'en',
  preferences   JSONB DEFAULT '{}',  -- UI, default model, RAG toggles
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);

-- CONVERSATIONS & MESSAGES
CREATE TABLE conversations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title         TEXT,
  model_id      TEXT,  -- e.g. openrouter/anthropic/claude-3.5-sonnet
  settings      JSONB DEFAULT '{}',  -- rag_enabled, web_search, temperature
  is_archived   BOOLEAN DEFAULT false,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_conversations_user ON conversations(user_id, updated_at DESC);

CREATE TABLE messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role            TEXT NOT NULL CHECK (role IN ('user','assistant','system','tool')),
  content         TEXT NOT NULL,
  content_json    JSONB,  -- structured parts, tool calls
  model_id        TEXT,
  token_count     INT,
  metadata        JSONB DEFAULT '{}',  -- citations, memory_refs, rag_chunks
  parent_id       UUID REFERENCES messages(id),  -- for branches
  created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);

-- USER MEMORIES (AI personalization — NOT notes)
CREATE TABLE user_memories (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  memory_type     TEXT NOT NULL,  -- preference, fact, goal, context
  content         TEXT NOT NULL,
  source_type     TEXT,  -- conversation, explicit, integration
  source_id       UUID,  -- conversation_id or message_id
  confidence      REAL DEFAULT 0.8 CHECK (confidence BETWEEN 0 AND 1),
  relevance_score REAL DEFAULT 1.0,
  is_pinned       BOOLEAN DEFAULT false,
  expires_at      TIMESTAMPTZ,  -- optional TTL
  embedding       vector(1536),  -- model-dependent dimension
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now(),
  deleted_at      TIMESTAMPTZ  -- soft delete
);
CREATE INDEX idx_memories_user ON user_memories(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_memories_embedding ON user_memories
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- NOTES (user-owned knowledge artifacts)
CREATE TABLE notes (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title           TEXT NOT NULL,
  content         TEXT,  -- markdown
  content_plain   TEXT,  -- stripped for FTS
  folder_id       UUID REFERENCES note_folders(id),
  note_type       TEXT DEFAULT 'note',  -- note, summary, flashcard, study_guide, etc.
  source_type     TEXT,  -- manual, chat, document, integration, ai_generated
  source_id       UUID,
  is_pinned       BOOLEAN DEFAULT false,
  metadata        JSONB DEFAULT '{}',
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now(),
  deleted_at      TIMESTAMPTZ
);
CREATE INDEX idx_notes_user ON notes(user_id, updated_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_notes_fts ON notes USING gin(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content_plain,'')));

CREATE TABLE note_folders (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  parent_id   UUID REFERENCES note_folders(id),
  name        TEXT NOT NULL,
  sort_order  INT DEFAULT 0
);

CREATE TABLE note_tags (
  note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
  tag     TEXT NOT NULL,
  PRIMARY KEY (note_id, tag)
);

CREATE TABLE note_links (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  target_note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  link_type     TEXT DEFAULT 'backlink',  -- backlink, embed
  UNIQUE(source_note_id, target_note_id)
);

CREATE TABLE note_versions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  note_id     UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  content     TEXT NOT NULL,
  version_num INT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- NOTE EMBEDDINGS (for RAG retrieval — separate from memory embeddings)
CREATE TABLE note_chunks (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  note_id     UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL,
  content     TEXT NOT NULL,
  metadata    JSONB DEFAULT '{}',
  embedding   vector(1536)
);

-- DOCUMENTS & RAG
CREATE TABLE documents (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename      TEXT NOT NULL,
  mime_type     TEXT,
  s3_key        TEXT NOT NULL,
  status        TEXT DEFAULT 'pending',  -- pending, processing, ready, failed
  byte_size     BIGINT,
  metadata      JSONB DEFAULT '{}',
  created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE document_chunks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id   UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index   INT NOT NULL,
  content       TEXT NOT NULL,
  page_number   INT,
  metadata      JSONB DEFAULT '{}',
  embedding     vector(1536)
);
CREATE INDEX idx_doc_chunks_embedding ON document_chunks
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- RETRIEVAL AUDIT (citations / traceability)
CREATE TABLE retrieval_logs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id      UUID REFERENCES messages(id),
  source_type     TEXT NOT NULL,  -- document, note, memory, web
  source_id       UUID,
  chunk_id        UUID,
  score           REAL,
  rank            INT,
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- MODEL ROUTING
CREATE TABLE model_registry (
  id              TEXT PRIMARY KEY,  -- openrouter/anthropic/claude-3.5-sonnet
  provider        TEXT NOT NULL,
  display_name    TEXT,
  capabilities    JSONB DEFAULT '[]',  -- chat, vision, tools, json
  cost_per_1k_in  REAL,
  cost_per_1k_out REAL,
  avg_latency_ms  INT,
  is_active       BOOLEAN DEFAULT true
);

CREATE TABLE user_model_preferences (
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
  default_model   TEXT REFERENCES model_registry(id),
  fallback_chain  JSONB DEFAULT '[]',  -- ordered model ids
  routing_policy  TEXT DEFAULT 'manual',  -- manual, cost, latency, auto
  PRIMARY KEY (user_id)
);

-- INTEGRATIONS
CREATE TABLE integrations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider      TEXT NOT NULL,  -- gmail, slack, notion, gdrive, gcal
  status        TEXT DEFAULT 'connected',
  scopes        TEXT[],
  metadata      JSONB DEFAULT '{}',
  created_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, provider)
);

CREATE TABLE integration_tokens (
  integration_id  UUID PRIMARY KEY REFERENCES integrations(id) ON DELETE CASCADE,
  access_token    TEXT NOT NULL,  -- encrypted at app layer
  refresh_token   TEXT,
  expires_at      TIMESTAMPTZ
);

CREATE TABLE integration_sync_records (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  integration_id  UUID REFERENCES integrations(id) ON DELETE CASCADE,
  external_id     TEXT NOT NULL,
  resource_type   TEXT,  -- email, page, file, event
  title           TEXT,
  snippet         TEXT,
  synced_at       TIMESTAMPTZ DEFAULT now(),
  metadata        JSONB DEFAULT '{}',
  UNIQUE(integration_id, external_id)
);

-- ANALYTICS
CREATE TABLE usage_events (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id),
  event_type    TEXT NOT NULL,  -- chat_completion, embedding, rag_query, web_search
  model_id      TEXT,
  tokens_in     INT,
  tokens_out    INT,
  cost_usd      REAL,
  latency_ms    INT,
  metadata      JSONB DEFAULT '{}',
  created_at    TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_usage_user_time ON usage_events(user_id, created_at DESC);

-- AGENTS (future)
CREATE TABLE agents (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
  name          TEXT NOT NULL,
  system_prompt TEXT,
  tools         JSONB DEFAULT '[]',
  model_id      TEXT,
  is_active     BOOLEAN DEFAULT true
);
```

---

## 8. Memory Architecture Design

### 8.1 Memory Layers

| Layer | Storage | TTL | Purpose |
|-------|---------|-----|---------|
| **STM (Short-Term)** | Redis + last N messages in PG | Session / last 20–50 msgs | Immediate chat context |
| **Working Memory** | Assembled per request | Ephemeral | Merged STM + retrieved LTM + RAG |
| **LTM (Long-Term)** | `user_memories` + embeddings | Durable | Preferences, facts, goals |
| **Episodic** | Conversation embeddings (optional table) | Durable | Semantic recall of past chats |

### 8.2 Memory vs Notes — Critical Separation

| Aspect | Memory | Notes |
|--------|--------|-------|
| **Owner** | Platform (AI context) | User (knowledge artifact) |
| **Purpose** | Personalize AI responses | Organize & retain knowledge |
| **User control** | View/edit/delete | Full CRUD + organization |
| **RAG role** | Injected as system context | Retrieved as citation sources |
| **Auto-created** | Yes (extraction pipeline) | Opt-in or explicit save |

### 8.3 Memory Write Rules

```
WRITE when:
  - User explicitly states preference ("I prefer Python", "Call me Alex")
  - User states durable fact ("I work at Acme", "My timezone is IST")
  - User sets goal ("I'm learning Rust")
  - Assistant infers high-confidence preference (confidence >= 0.85) AND user didn't contradict

DO NOT WRITE when:
  - Transient context ("I'm tired today")
  - Hypotheticals ("If I were...")
  - Low confidence (< 0.6)
  - Duplicate of existing memory (cosine similarity > 0.92)
  - User disabled memory for conversation
```

### 8.4 Memory Update Rules

```
UPDATE when:
  - New info contradicts old → supersede (soft-delete old, create new with higher confidence)
  - User edits memory in UI → set confidence = 1.0, source = explicit
  - Reinforcement: same fact mentioned again → boost confidence (+0.05, cap 1.0)

DECAY:
  - Unpinned memories: relevance_score *= 0.99 per 30 days without retrieval
  - Retrieved memories: relevance_score = min(1.0, relevance_score + 0.1)
```

### 8.5 Memory Deletion Rules

```
DELETE when:
  - User explicitly deletes
  - GDPR account deletion (cascade)
  - Superseded by contradiction
  - Expires_at reached (for temporary context memories)
  - confidence < 0.3 AND not pinned AND age > 90 days
```

### 8.6 Memory Retrieval Flow

```
1. Embed current user message
2. Vector search user_memories (top 10, min score 0.75)
3. Boost: pinned (+0.2), recent (+0.1), high confidence (+0.1)
4. Optional: episodic conversation search (top 3 conversation summaries)
5. Deduplicate and rank → inject top 5–8 into system prompt (~500 tokens max)
```

### 8.7 Post-Turn Memory Extraction (Async Worker)

```
After assistant response:
  1. LLM structured extraction (JSON schema: memories[])
  2. Validate against write rules
  3. Dedupe against existing embeddings
  4. Insert/update user_memories
  5. Generate embeddings (batch)
```

---

## 9. RAG Architecture Design

### 9.1 Pipeline Overview

```
Ingest → Parse → Chunk → Embed → Index → Retrieve → Rerank → Assemble → Cite
```

### 9.2 Document Ingestion

| Step | Implementation |
|------|----------------|
| Upload | Presigned S3 URL → `documents` row (status=pending) |
| Queue | Celery job `process_document` |
| Parse | Unstructured.io or pdfplumber + python-docx |
| Clean | Strip headers/footers, normalize whitespace |
| Metadata | page, section, source filename, user_id |

### 9.3 Chunking Strategy

| Content Type | Strategy | Size |
|--------------|----------|------|
| PDF/DOCX | Recursive character splitter | 512 tokens, 64 overlap |
| Markdown/Notes | Header-aware (H1/H2 boundaries) | 400–600 tokens |
| Code | AST-aware or function-level | Variable |
| Email (Gmail) | Per-thread or per-message | 300 tokens |

### 9.4 Embedding Generation

- **Model:** `text-embedding-3-small` via OpenRouter (or local `bge-small` for cost)
- **Batch:** 100 chunks per API call
- **Store:** `document_chunks.embedding`, `note_chunks.embedding`
- **Versioning:** `embedding_model` column for re-index migrations

### 9.5 Retrieval

```
Query embedding
  → Parallel search:
      - document_chunks (top 20)
      - note_chunks (top 10) [if notes RAG enabled]
      - integration_sync_records (FTS top 5) [if integrations enabled]
  → Merge candidates (max 30)
  → Metadata filter: user_id, not deleted, status=ready
```

### 9.6 Reranking

- **MVP:** Cross-encoder via Cohere Rerank API or `bge-reranker-base` (self-hosted)
- **Input:** query + top 30 chunks
- **Output:** top 5–8 chunks (score threshold 0.5)

### 9.7 Prompt Assembly

```
[System]
You are a personal AI assistant. Use the following context when relevant.
Cite sources using [1], [2] notation.

[User Memory]        ← from Memory Service (not RAG citations)
{memories}

[Retrieved Context]  ← from RAG
[1] (document: report.pdf, p.3) {chunk text}
[2] (note: "Rust Study Guide") {chunk text}

[Conversation History]
{last N messages}

[User Message]
{message}
```

### 9.8 Citation / Traceability

- Every retrieved chunk logged in `retrieval_logs`
- Assistant `metadata.citations[]` on message: `{source_type, source_id, chunk_id, title, excerpt}`
- UI renders clickable citations → open document viewer or note

### 9.9 Notes in RAG (Separate Index Path)

Notes have their own chunk table (`note_chunks`) — **never mixed with `user_memories`**.

When user saves note from chat:
1. Create `notes` row
2. Async: chunk + embed → `note_chunks`
3. Available for RAG immediately after indexing

---

## 10. Model Routing and Fallback Strategy

### 10.1 Provider Abstraction

Use **LiteLLM** or a thin custom adapter:

```python
# Unified interface
async def complete(model_id: str, messages: list, stream: bool = True) -> AsyncIterator[str]:
    provider, model = parse_model_id(model_id)  # openrouter/anthropic/claude-3.5-sonnet
    if provider == "openrouter":
        return openrouter_client.chat(model, messages, stream)
    elif provider == "direct_anthropic":
        return anthropic_client.chat(model, messages, stream)
    ...
```

### 10.2 Routing Policies

| Policy | Behavior |
|--------|----------|
| **manual** | User-selected model only; fallback on error |
| **cost** | Route to cheapest capable model for task type |
| **latency** | Route to lowest p95 latency model |
| **auto** | Task classifier picks model (simple → small, complex → large) |
| **user_override** | Per-message model override always wins |

### 10.3 Fallback Chain

```
Primary: user-selected model
  ↓ (429, 5xx, timeout 30s)
Fallback 1: user.fallback_chain[0] or platform default
  ↓
Fallback 2: user.fallback_chain[1]
  ↓
Last resort: gpt-4o-mini / claude-haiku (fast, cheap, reliable)
```

### 10.4 Error Handling

| Error | Action |
|-------|--------|
| 429 Rate limit | Exponential backoff (1s, 2s, 4s) → fallback model |
| 503 Unavailable | Immediate fallback |
| Context length exceeded | Summarize history → retry with smaller model |
| Invalid API key | Alert ops; fail with clear user message |

### 10.5 Cost-Aware Routing Example

```
if tokens_estimated < 2000 and task == "simple_qa":
    model = "openrouter/google/gemini-flash-1.5"
elif requires_tools or requires_json:
    model = "openrouter/anthropic/claude-3.5-sonnet"
else:
    model = user.default_model
```

### 10.6 Model Registry (Seed Data)

| model_id | Provider | Use Case |
|----------|----------|----------|
| openrouter/anthropic/claude-3.5-sonnet | Anthropic | Default quality |
| openrouter/openai/gpt-4o | OpenAI | Vision, tools |
| openrouter/google/gemini-2.0-flash | Google | Fast, cheap |
| openrouter/meta-llama/llama-3.3-70b | Groq via OR | Open, fast |
| openrouter/deepseek/deepseek-chat | DeepSeek | Cost-efficient reasoning |

---

## 11. Web Search Integration Strategy

### 11.1 When to Search

| Trigger | Mechanism |
|---------|-----------|
| User enables "Web search" toggle | Always augment query |
| Model tool call `web_search` | Agent invokes search tool |
| Heuristic | Query contains "latest", "today", "current", year 2025+ |
| User slash command | `/search {query}` |

### 11.2 Provider Stack

| Priority | Provider | Why |
|----------|----------|-----|
| Primary | **Tavily API** | Built for AI agents, returns clean snippets |
| Fallback | Serper (Google SERP) | Broad coverage |
| Fallback 2 | Brave Search API | Privacy-friendly |

### 11.3 Flow

```
1. Rewrite query (optional LLM step for better search terms)
2. Call search API (top 5 results)
3. Fetch page content (readability extraction, max 3 pages)
4. Chunk + inject as [Web: title](url) context
5. Log in retrieval_logs (source_type=web)
6. Cite URLs in response
```

### 11.4 Caching

- Redis cache: `search:{hash(query)}` TTL 1 hour
- Reduces cost for repeated queries

---

## 12. Third-Party Integration Strategy

### 12.1 Integration Architecture

```
┌──────────────┐     OAuth 2.0      ┌─────────────────┐
│   React UI   │ ───────────────► │ Integration Svc │
└──────────────┘                  └────────┬────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
              ┌─────▼─────┐         ┌──────▼──────┐        ┌──────▼──────┐
              │ Gmail API │         │ Slack API   │        │ Notion API  │
              └───────────┘         └─────────────┘        └─────────────┘
```

### 12.2 Per-Integration Plan

| Integration | OAuth Scopes | Sync Strategy | Chat Use |
|-------------|--------------|---------------|----------|
| **Gmail** | `gmail.readonly` | Incremental sync via historyId | "Summarize unread", search emails |
| **Slack** | `channels:history`, `users:read` | Webhook + periodic backfill | Channel summaries, search |
| **Notion** | `read_content` | Poll changed pages (cursor) | Import pages to notes/docs |
| **Google Drive** | `drive.readonly` | Watch API or poll | Document ingestion to RAG |
| **Google Calendar** | `calendar.readonly` | Sync next 30 days events | "What's on my calendar?" |

### 12.3 Token Security

- Encrypt `access_token` / `refresh_token` with AES-256-GCM (KMS-managed key)
- Auto-refresh before expiry
- Revoke on disconnect

### 12.4 MCP-Style Plugin Runtime (Phase 3+)

```
plugins/
  manifest.json       # name, version, permissions, tools[]
  connector.py        # implements search, fetch, action handlers
  
Runtime:
  - Sandboxed execution (gVisor / WASM for untrusted)
  - Permission model: read_email, write_calendar, etc.
  - Tool registry exposed to AI Orchestrator
```

Compatible with emerging **MCP (Model Context Protocol)** — build an MCP server that wraps your Integration Service.

---

## 13. Analytics Architecture

### 13.1 Event Collection

```
Every API call → usage_events (PostgreSQL, hot)
              → async flush → S3 parquet (cold, daily)
              → ClickHouse (Phase 3, dashboards)
```

### 13.2 Key Metrics

| Dashboard | Metrics |
|-----------|---------|
| **Usage** | Messages/day, active users, conversations |
| **Models** | Tokens in/out per model, cost USD |
| **Performance** | p50/p95 latency (TTFT, total), error rate |
| **RAG** | Retrieval count, avg chunks, rerank scores |
| **Memory** | Memories created/updated/deleted, retrieval hit rate |
| **Integrations** | Sync success rate, last sync time |

### 13.3 Cost Attribution

```sql
SELECT model_id, SUM(cost_usd), SUM(tokens_in + tokens_out)
FROM usage_events
WHERE user_id = $1 AND created_at > now() - interval '30 days'
GROUP BY model_id;
```

### 13.4 Build vs Buy

| Component | Recommendation |
|-----------|----------------|
| Event storage (MVP) | PostgreSQL `usage_events` |
| Dashboards (MVP) | Custom React charts (Recharts) |
| Scale analytics | ClickHouse + Grafana or Metabase |
| Product analytics | PostHog (optional, self-host) |

---

## 14. API Design Outline

### 14.1 API Conventions

- Base: `https://api.yourplatform.com/v1`
- Auth: `Authorization: Bearer <jwt>`
- Pagination: `?cursor=&limit=20`
- Errors: RFC 7807 Problem Details

### 14.2 Core Endpoints

#### Auth & Profile
```
POST   /auth/register
POST   /auth/login
GET    /users/me
PATCH  /users/me/profile
GET    /users/me/preferences
PUT    /users/me/preferences
```

#### Chat
```
GET    /conversations
POST   /conversations
GET    /conversations/{id}
PATCH  /conversations/{id}
DELETE /conversations/{id}
GET    /conversations/{id}/messages
POST   /conversations/{id}/messages          # non-streaming
POST   /conversations/{id}/messages/stream   # SSE/WebSocket
POST   /conversations/{id}/messages/{msg_id}/regenerate
```

#### Models
```
GET    /models                               # list from model_registry
GET    /users/me/model-preferences
PUT    /users/me/model-preferences
```

#### Memory
```
GET    /memories
POST   /memories                             # explicit user memory
GET    /memories/{id}
PATCH  /memories/{id}
DELETE /memories/{id}
POST   /memories/search                      # semantic search (debug/UI)
```

#### Notes
```
GET    /notes
POST   /notes
GET    /notes/{id}
PATCH  /notes/{id}
DELETE /notes/{id}
GET    /notes/{id}/versions
POST   /notes/{id}/versions/{v}/restore
GET    /notes/folders
POST   /notes/folders
GET    /notes/tags
POST   /notes/from-message                   # save message to note
POST   /notes/ai-transform                   # {note_id, transform: "flashcards"}
GET    /notes/search?q=&semantic=true
GET    /notes/graph                          # backlinks graph
```

#### Documents & RAG
```
POST   /documents/upload-url                 # presigned S3
POST   /documents                            # confirm upload
GET    /documents
GET    /documents/{id}
DELETE /documents/{id}
POST   /documents/{id}/reindex
```

#### Integrations
```
GET    /integrations
POST   /integrations/{provider}/connect      # returns OAuth URL
GET    /integrations/{provider}/callback
DELETE /integrations/{provider}
POST   /integrations/{provider}/sync
GET    /integrations/{provider}/resources
```

#### Web Search
```
POST   /search                               # {query, max_results}
```

#### Analytics
```
GET    /analytics/usage?from=&to=
GET    /analytics/models
GET    /analytics/costs
```

#### Agents (Phase 2+)
```
GET    /agents
POST   /agents
POST   /agents/{id}/run
```

### 14.3 WebSocket Events

```
ws://api/v1/chat/stream
  → client: {conversation_id, content, model_id?, rag_sources?, web_search?}
  ← server: {type: "token", data: "..."}
  ← server: {type: "citation", data: {...}}
  ← server: {type: "done", data: {message_id, usage}}
```

---

## 15. Security and Access Control Design

### 15.1 Authentication

- JWT access tokens (15 min) + refresh tokens (7 days, httpOnly cookie)
- Or Clerk/Auth0 for MVP
- MFA optional (TOTP) in Phase 2

### 15.2 Authorization

- Row-level security: every query scoped by `user_id`
- PostgreSQL RLS policies on all user tables
- Integration tokens encrypted at application layer

### 15.3 Data Protection

| Data | Protection |
|------|------------|
| At rest | PostgreSQL TDE or disk encryption; S3 SSE-S3 |
| In transit | TLS 1.3 everywhere |
| Secrets | AWS Secrets Manager / Vault |
| PII | Minimize storage; support export/delete |

### 15.4 API Security

- Rate limiting: 60 req/min user, 10 chat/min
- Input sanitization (XSS in notes — use DOMPurify)
- CORS whitelist
- OWASP top 10 checklist

### 15.5 AI-Specific Security

- Prompt injection mitigation: separate system/user boundaries; sandbox tool outputs
- Integration actions require user confirmation (write ops)
- Audit log for sensitive actions

---

## 16. Deployment and Scaling Plan

### 16.1 MVP Infrastructure (Single Region)

```
┌─────────────────────────────────────────┐
│  Vercel / Cloudflare Pages  (React)     │
├─────────────────────────────────────────┤
│  Railway / Fly.io / ECS     (FastAPI)   │
│  ├── API containers (2 replicas)        │
│  └── Celery workers (2)                 │
├─────────────────────────────────────────┤
│  RDS PostgreSQL 16 + pgvector           │
│  ElastiCache Redis                      │
│  S3 bucket                              │
└─────────────────────────────────────────┘
```

### 16.2 Production (Multi-Region Ready)

| Component | Scaling |
|-----------|---------|
| API | Horizontal pods + HPA (CPU/memory) |
| Workers | Queue-depth based scaling |
| PostgreSQL | Read replicas; connection pooling (PgBouncer) |
| Redis | Cluster mode |
| Vector search | Migrate hot vectors to Qdrant if > 10M |
| CDN | CloudFront for static assets |

### 16.3 CI/CD

```
GitHub → GitHub Actions → test → build Docker → deploy staging → smoke test → prod
```

### 16.4 Environments

`dev` → `staging` → `production` (separate DB, S3 buckets, API keys)

---

## 17. Knowledge & Notes System — Deep Dive

### 17.1 Note Lifecycle

```
CREATE (manual | from_chat | from_doc | from_integration | ai_generated)
  → DRAFT (auto-save every 2s)
  → PUBLISHED (user saves)
  → INDEXING (async chunk + embed)
  → INDEXED (available for RAG + search)
  → ARCHIVED / DELETED (soft delete, remove from RAG index)
```

### 17.2 AI Transform Types

| Transform | Output `note_type` | Structure |
|-----------|-------------------|-----------|
| Summary | `summary` | Bullet points |
| Study guide | `study_guide` | Sections + key concepts |
| Flashcards | `flashcard` | JSON `{q, a}[]` in metadata |
| Interview Qs | `interview_questions` | Numbered list |
| Revision sheet | `revision_sheet` | Compact facts table |
| Knowledge article | `article` | Full structured doc |

API: `POST /notes/ai-transform` with `{source: message_id|conversation_id, transform_type}`

### 17.3 Backlinks & Graph

- Parse `[[Note Title]]` or `[[uuid]]` on save
- Upsert `note_links` table
- `GET /notes/graph` returns nodes + edges for Obsidian-style graph view

### 17.4 UX Flows

**Flow A: Save message to note**
1. User clicks "Save to Notes" on message
2. Modal: choose folder, add tags, edit title
3. Note created with `source_type=chat`, `source_id=message_id`
4. Toast: "Saved. Indexing for search..."

**Flow B: Conversation → Study guide**
1. User clicks "Create Study Guide" on conversation
2. Backend runs transform job (selected model)
3. New note appears in folder "AI Generated"
4. User edits and organizes

**Flow C: Semantic search across notes**
1. User types in Notes search bar
2. Toggle: Full-text / Semantic
3. Results ranked with highlights + backlinks preview

### 17.5 Notes Retrieval in Chat

User can @-mention notes or enable "Include my notes" in chat settings → RAG pulls from `note_chunks` only.

---

## 18. Recommended Folder Structure

```
paios/                          # Personal AI Operating System
├── apps/
│   ├── web/                    # React frontend
│   │   ├── src/
│   │   │   ├── features/
│   │   │   │   ├── chat/
│   │   │   │   ├── notes/
│   │   │   │   ├── documents/
│   │   │   │   ├── memory/
│   │   │   │   ├── integrations/
│   │   │   │   ├── analytics/
│   │   │   │   └── settings/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── api/
│   │   │   └── stores/
│   │   └── package.json
│   └── api/                    # FastAPI backend
│       ├── app/
│       │   ├── main.py
│       │   ├── api/v1/
│       │   │   ├── chat.py
│       │   │   ├── notes.py
│       │   │   ├── memories.py
│       │   │   ├── documents.py
│       │   │   ├── models.py
│       │   │   ├── integrations.py
│       │   │   ├── search.py
│       │   │   └── analytics.py
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   ├── security.py
│       │   │   └── deps.py
│       │   ├── services/
│       │   │   ├── orchestrator.py      # main AI pipeline
│       │   │   ├── model_router.py
│       │   │   ├── memory_service.py
│       │   │   ├── rag_service.py
│       │   │   ├── notes_service.py
│       │   │   ├── embedding_service.py
│       │   │   ├── web_search_service.py
│       │   │   └── integration_service.py
│       │   ├── providers/
│       │   │   ├── openrouter.py
│       │   │   ├── litellm_adapter.py
│       │   │   └── base.py
│       │   ├── integrations/
│       │   │   ├── gmail.py
│       │   │   ├── slack.py
│       │   │   ├── notion.py
│       │   │   ├── gdrive.py
│       │   │   └── gcal.py
│       │   ├── workers/
│       │   │   ├── celery_app.py
│       │   │   ├── document_processor.py
│       │   │   ├── memory_extractor.py
│       │   │   ├── note_indexer.py
│       │   │   └── integration_sync.py
│       │   ├── models/          # SQLAlchemy ORM
│       │   └── schemas/         # Pydantic
│       ├── migrations/          # Alembic
│       ├── tests/
│       └── pyproject.toml
├── packages/
│   └── shared-types/            # TypeScript types shared with frontend
├── infra/
│   ├── docker/
│   ├── terraform/
│   └── k8s/
├── docs/
│   ├── architecture.md
│   ├── api-spec.yaml             # OpenAPI
│   └── adr/                      # Architecture Decision Records
└── docker-compose.yml            # local dev: pg, redis, minio, api, worker
```

---

## 19. Build First vs Outsource vs Custom-Owned

| Component | Build | Outsource/Buy | Why |
|-----------|-------|---------------|-----|
| **Chat UI** | ✅ Custom | | Core product differentiation |
| **Notes/KB UI** | ✅ Custom | | Personal OS experience |
| **Orchestration pipeline** | ✅ Custom | | Your IP; provider-agnostic |
| **Memory logic** | ✅ Custom | | Core differentiation |
| **RAG pipeline** | ✅ Custom | | Data ownership |
| **Model inference** | | ✅ OpenRouter | Commodity; don't host GPUs |
| **Embeddings API** | | ✅ OpenRouter/OpenAI | Or self-host later |
| **Web search** | Thin wrapper | ✅ Tavily/Serper | Not worth building |
| **Auth (MVP)** | | ✅ Clerk | Speed; migrate later |
| **Email/Slack OAuth** | ✅ Custom connectors | APIs are standard | |
| **Object storage** | | ✅ S3/MinIO | Commodity |
| **Vector DB (MVP)** | ✅ pgvector | | Owned data |
| **Analytics dashboards** | ✅ Custom (MVP) | PostHog optional | |
| **Document parsing** | Thin wrapper | ✅ Unstructured.io | Complex formats |
| **Reranking** | Optional self-host | ✅ Cohere Rerank | |

**Always custom-owned:** conversations, messages, memories, notes, embeddings metadata, user profiles, retrieval logs, integration sync data.

---

## 20. MVP Roadmap (8–12 Weeks)

### Week 1–2: Foundation
- [ ] Monorepo setup, Docker Compose (Postgres+pgvector, Redis, MinIO)
- [ ] FastAPI skeleton, auth (Clerk or JWT)
- [ ] React app shell: layout, routing, auth
- [ ] DB migrations: users, conversations, messages

### Week 3–4: Chat + Models
- [ ] OpenRouter integration via LiteLLM
- [ ] Model registry + user model selection
- [ ] Streaming chat (SSE)
- [ ] Conversation CRUD
- [ ] Basic usage logging

### Week 5–6: Memory
- [ ] STM: last N messages
- [ ] Memory extraction worker
- [ ] `user_memories` CRUD UI
- [ ] Semantic memory retrieval in chat

### Week 7–8: RAG + Documents
- [ ] S3 upload flow
- [ ] Document parsing + chunking worker
- [ ] Embedding pipeline
- [ ] RAG retrieval + citations in chat
- [ ] Document management UI

### Week 9–10: Notes
- [ ] Notes CRUD, folders, tags
- [ ] Save message to note
- [ ] Note chunking + embedding
- [ ] Full-text + semantic search
- [ ] AI transform: summary + study guide

### Week 11–12: Polish + Analytics
- [ ] Model fallback chain
- [ ] Usage/cost dashboard
- [ ] Web search integration
- [ ] Error handling, rate limits
- [ ] Deploy to staging

**MVP delivers:** Chat + multi-model + memory + documents RAG + notes + basic analytics.

---

## 21. Phase-Wise Build Plan (MVP → Full Platform)

### Phase 1: Personal AI Core (Months 1–3) — MVP above

### Phase 2: Knowledge OS (Months 4–5)
- Backlinks + graph view
- Note version history
- All AI transforms (flashcards, interview Qs)
- Conversation branching
- Reranking (Cohere)
- Cost-aware routing policies

### Phase 3: Connected OS (Months 6–8)
- Gmail + Google Drive + Calendar integrations
- Slack integration
- Notion import
- Integration data in RAG
- Web search heuristics + caching

### Phase 4: Agent Platform (Months 9–11)
- Tool registry (search, notes, email, calendar)
- Agent definitions + runs
- MCP server exposing platform tools
- Plugin manifest system
- Multi-step agent workflows

### Phase 5: Scale & Enterprise (Months 12+)
- ClickHouse analytics
- S3 data lake + batch re-embedding
- Qdrant migration if needed
- Team workspaces (multi-tenant)
- SSO/SAML
- Audit logs + compliance exports

---

## 22. Development Milestones Checklist

| Milestone | Success Criteria |
|-----------|------------------|
| **M1: Hello Chat** | User can log in, send message, get streamed GPT/Claude response |
| **M2: Model Swap** | User switches model mid-conversation, no data loss |
| **M3: Memory Works** | AI remembers name/preference across new conversations |
| **M4: RAG Works** | Upload PDF, ask question, get cited answer |
| **M5: Notes Live** | Save chat to note, search finds it semantically |
| **M6: Resilient** | Provider outage triggers fallback automatically |
| **M7: Connected** | Gmail emails appear in chat context |
| **M8: Agent Ready** | Agent completes multi-step task with tools |

---

## 23. Step-by-Step Build Order (Practical Sequence)

```
1.  Infrastructure (Docker, PG, Redis, S3)
2.  Auth + user profiles
3.  Conversations + messages API
4.  Model gateway (OpenRouter) + streaming
5.  React chat UI
6.  Model selector + registry
7.  Usage event logging
8.  Memory tables + extraction worker
9.  Memory injection in orchestrator
10. Memory management UI
11. Document upload + S3
12. Document processing worker
13. Embeddings service
14. RAG retrieval + prompt assembly
15. Citations in UI
16. Notes schema + CRUD API
17. Notes editor UI (Markdown)
18. Note indexing worker
19. Save-to-note from chat
20. Notes search (FTS + semantic)
21. AI note transforms
22. Web search service
23. Model fallback router
24. Analytics API + dashboard
25. Gmail OAuth + sync
26. Slack, Notion, Drive, Calendar
27. Agent framework
28. MCP plugin runtime
```

---

## 24. Key Architecture Decisions (ADRs to Document)

1. **FastAPI over NestJS** — AI ecosystem fit
2. **PostgreSQL + pgvector for MVP** — simplicity, ownership
3. **OpenRouter as primary gateway** — multi-provider without lock-in
4. **Memory ≠ Notes** — separate tables, separate retrieval paths
5. **Async workers for all heavy lifting** — embeddings, ingestion, extraction
6. **Citations via retrieval_logs** — full traceability
7. **LiteLLM for provider abstraction** — battle-tested fallback

---

## Next Steps for You

1. **Save this document** as `docs/PAIOS-Architecture.md` in your repo.
2. **Switch to Agent mode** and ask: *"Create the project scaffold from the PAIOS architecture doc"* — I can generate the monorepo, Docker Compose, DB migrations, and API skeleton.
3. **To get a PDF:** In Agent mode, ask me to export this to PDF (via `pandoc` or `weasyprint`), or paste into Notion/Google Docs and export.

If you want, I can next produce:
- **OpenAPI 3.0 spec** for all endpoints
- **Alembic migration files** (SQL)
- **Docker Compose** for local dev
- **Detailed orchestrator pseudocode** for the chat pipeline

Say which slice you want to implement first (Chat, Notes, or RAG), and switch to Agent mode when you're ready to build.

