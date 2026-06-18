# Phase 1 Hardening Suggestions

These are recommended improvements after package installation and first local run.

## Backend

- Add route tests for auth, conversations, messages, streaming, tools, and run details.
- Add Redis-backed rate limiting per user and per IP.
- Add structured logging with `request_id`, `user_id`, `conversation_id`, and `model_run_id`.
- Add provider timeout and retry policy for OpenRouter calls.
- Add token counting with a real tokenizer instead of the current heuristic.
- Add model pricing refresh from OpenRouter metadata if available.
- Add pagination for conversations and messages.
- Add soft-delete or archive-only behavior for conversations if you want recoverability.

## Frontend

- Add toast notifications for auth, streaming, and save errors.
- Add loading skeletons for conversations and messages.
- Add retry and regenerate behavior for the last assistant message.
- Add conversation rename and delete interactions in the sidebar.
- Add keyboard shortcuts for mode switching and new chat.
- Add mobile responsive layout after desktop flow is stable.

## Infrastructure

- Add Docker health check for the backend `/health` route.
- Add a CI workflow that runs backend syntax checks, backend tests, and frontend build.
- Add separate `.env.example` files for backend and frontend if deployment targets diverge.
