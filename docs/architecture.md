# PAIOS Architecture

Phase 1 builds the Chat Core. The app stores users, conversations, messages, model registry rows, and model run details in PostgreSQL. Redis is included for rate limiting and future queues.

## Interaction Modes

### Chat Mode

The backend stores the user message, loads the last 20 conversation messages, formats them for OpenRouter, streams assistant tokens through Server-Sent Events, stores the assistant message, and records run details.

### Web Search Mode

The backend stores the user message, ignores conversation history, performs DuckDuckGo search through LangChain, emits sources, builds a source-grounded prompt, streams the answer, and stores sources on the assistant message.

### Tool Mode

The backend stores the user message, loads the last 10 messages, sends registered OpenAI-compatible tool definitions to OpenRouter, executes one selected local tool, emits raw tool output, asks the model for the final response, then stores tool call metadata.

## Future Plug-In Points

- Phase 2 memory plugs into `app/core/context_builder.py`.
- Phase 3 RAG plugs into `app/core/context_builder.py`.
- Phase 5 integrations plug into `app/tools/registry.py` and `app/tools/executor.py`.
