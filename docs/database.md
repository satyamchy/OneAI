# Database Schema

## users

Stores account identity, password hash, timestamps, and optional profile URLs.

## conversations

Stores user-owned chat threads, selected model, current `interaction_mode`, timestamps, and archive state.

## messages

Stores user, assistant, and system messages. Assistant messages can include `model_used`, `mode_used`, `tool_calls_json`, and `search_sources_json`.

## model_registry

Stores active model metadata for UI selection and later pricing calculations.

## model_runs

Stores traceable model execution metadata: requested model, actual model, provider, tokens, latency, estimated cost, status, fallback reason, and request ID.
