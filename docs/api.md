# API Reference

All backend routes are mounted under `/v1`.

## Auth

- `POST /v1/auth/register`: create account and return JWT.
- `POST /v1/auth/login`: authenticate and return JWT.
- `GET /v1/auth/me`: return current user.

## Conversations

- `GET /v1/conversations`: list conversations.
- `POST /v1/conversations`: create conversation.
- `GET /v1/conversations/{conversation_id}`: read conversation.
- `PATCH /v1/conversations/{conversation_id}`: update title, model, mode, or archive flag.
- `DELETE /v1/conversations/{conversation_id}`: delete conversation.

## Messages

- `GET /v1/conversations/{conversation_id}/messages`: list messages.
- `POST /v1/conversations/{conversation_id}/messages`: create a non-streaming message.
- `POST /v1/conversations/{conversation_id}/messages/stream`: stream mode-aware assistant response using `text/event-stream`.

## Models

- `GET /v1/models`: list active model registry rows.

Every JSON response includes `request_id` where applicable. Streaming responses include an `X-Request-ID` header and SSE events: `meta`, `sources`, `tool_call`, `token`, and `done`.


## Model Runs

- `GET /v1/model-runs/{run_id}`: fetch full model run metadata for a run owned by the current user.

## Streaming Events

The streaming endpoint emits these Server-Sent Events:

- `meta`: request ID, mode, and selected model.
- `sources`: web search sources for Web Search mode.
- `tool_call`: raw tool call details for Tool mode.
- `token`: streamed assistant token.
- `error`: readable failure message plus run ID when provider/tool/search fails.
- `done`: final message ID, run ID, and request ID.
