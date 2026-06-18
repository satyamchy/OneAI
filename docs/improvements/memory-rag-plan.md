# Memory and RAG-Based Memory Plan

This guide explains how to add memory later without rewriting the Phase 1 chat pipeline.

## Goals

- Short-term context remains conversation history from `messages`.
- Long-term memory stores durable facts about the user, preferences, projects, and decisions.
- RAG memory stores searchable notes, documents, webpages, and extracted knowledge chunks.
- Context injection happens inside `backend/app/core/context_builder.py` so all modes can evolve cleanly.

## Suggested Future Tables

### memories

- `id`: UUID primary key.
- `user_id`: owner.
- `memory_type`: `preference`, `fact`, `project`, `decision`, `profile`, or `custom`.
- `content`: plain text memory.
- `source_message_id`: optional source message.
- `confidence`: numeric confidence score.
- `is_pinned`: force-inject important memories.
- `created_at` and `updated_at`.

### documents

- `id`: UUID primary key.
- `user_id`: owner.
- `title`: document title.
- `source_type`: `note`, `url`, `file`, `email`, `notion`, etc.
- `source_uri`: optional origin URL or integration ID.
- `raw_text`: extracted content.
- `created_at` and `updated_at`.

### document_chunks

- `id`: UUID primary key.
- `document_id`: parent document.
- `user_id`: owner for filtering.
- `chunk_text`: searchable chunk.
- `embedding`: vector column if using pgvector later.
- `metadata_json`: section, page, URL, timestamps.
- `created_at`.

## Backend Modules To Add Later

```text
backend/app/memory/
├── memory_service.py
├── memory_extractor.py
└── memory_prompt.py

backend/app/rag/
├── document_service.py
├── chunker.py
├── embeddings.py
├── retriever.py
└── rag_prompt.py
```

## Context Builder Hook

Add memory in `backend/app/core/context_builder.py`:

```python
# TODO Phase 2: inject pinned and relevant memories.
memories = await memory_service.get_relevant_memories(user_id=user_id, query=latest_prompt, db=db)

# TODO Phase 3: inject retrieved RAG chunks.
chunks = await rag_service.retrieve_chunks(user_id=user_id, query=latest_prompt, db=db)
```

## Recommended Retrieval Behavior

- Chat mode: use conversation history, pinned memories, and top RAG chunks.
- Web Search mode: stay stateless by default, but optionally allow a future setting to include profile memory.
- Tools mode: use short history, pinned memories, and tool-relevant memories.

## Memory Extraction Flow

1. After assistant response completes, run a background memory extractor.
2. Ask the extractor whether the conversation contains durable memory.
3. Store only stable facts, preferences, and decisions.
4. Avoid storing sensitive data unless the user explicitly asks.
5. Let the UI show and delete saved memories later.
