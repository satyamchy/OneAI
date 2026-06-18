# Tools Extension Guide

Phase 1 tools are registered in OpenAI function-calling format and executed locally. Future tools should plug into the same registry and executor.

## Add A New Tool

1. Add the OpenAI-compatible tool schema in `backend/app/tools/registry.py`.
2. Add an implementation file under `backend/app/tools/implementations/`.
3. Add one branch in `backend/app/tools/executor.py`.
4. Return raw string output from the tool implementation.
5. Let the existing Tool mode pipeline send the result back to the model.

## Example Tool Shape

```python
{
    "type": "function",
    "function": {
        "name": "gmail_search",
        "description": "Searches Gmail messages for the authenticated user",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Gmail search query"}
            },
            "required": ["query"]
        }
    }
}
```

## Tool Safety Rules

- Read-only tools can execute immediately.
- Write tools, such as email sending or calendar edits, should require user confirmation.
- Store raw tool calls in `messages.tool_calls_json` for auditability.
- Add per-tool timeouts so one slow integration does not block the stream forever.
- Never put API keys in tool schemas; load secrets from `config.py`.

## Future Tool Categories

- Gmail reader and sender.
- Notion page fetcher.
- Slack search.
- Calendar reader and event creator.
- Local file note search.
- Browser URL reader.
