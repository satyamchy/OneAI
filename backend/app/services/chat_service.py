import json
import time
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.chains.message_chain import build_provider_messages
from app.chains.title_chain import generate_fallback_title
from app.config import settings
from app.core.constants import InteractionMode, MessageRole, RunStatus
from app.core.context_builder import build_context
from app.models.conversation import Conversation
from app.providers.openrouter import OpenRouterProvider
from app.services.message_service import create_message
from app.services.run_service import record_model_run
from app.services.search_service import prepare_search_prompt
from app.services.tool_service import get_tool_definitions, run_tool_call
from app.utils.token_counter import estimate_tokens

# Formats one Server-Sent Events payload line for the streaming response.
def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

# Streams provider tokens into the response while collecting the final text.
async def stream_provider_tokens(provider: OpenRouterProvider, provider_messages: list[dict], selected_model: str) -> AsyncIterator[str]:
    async for token in provider.stream_chat(provider_messages, selected_model):
        yield token

# Streams a mode-aware model response and persists messages plus run metadata.
async def stream_chat_response(db: AsyncSession, conversation: Conversation, user_id, content: str, model: str | None, mode: InteractionMode | None, request_id: str) -> AsyncIterator[str]:
    selected_mode = mode or conversation.interaction_mode or InteractionMode.CHAT
    selected_model = model or conversation.selected_model or settings.openrouter_default_model
    provider = OpenRouterProvider()
    started_at = time.perf_counter()
    assistant_text = ""
    tool_payload = None
    search_sources = None

    await create_message(db, conversation.id, MessageRole.USER, content, mode_used=selected_mode)
    if conversation.title == "New Conversation":
        conversation.title = generate_fallback_title(content)
        await db.commit()

    yield sse("meta", {"request_id": request_id, "mode": selected_mode, "model": selected_model})

    try:
        context = await build_context(conversation.id, user_id, selected_mode, db)

        if selected_mode == InteractionMode.WEB_SEARCH:
            search_prompt, search_sources = await prepare_search_prompt(content)
            yield sse("sources", {"sources": search_sources})
            provider_messages = [{"role": "user", "content": search_prompt}]
            async for token in stream_provider_tokens(provider, provider_messages, selected_model):
                assistant_text += token
                yield sse("token", {"token": token})

        elif selected_mode == InteractionMode.TOOLS:
            provider_messages = build_provider_messages(context, content)
            planning = await provider.complete_chat(provider_messages, selected_model, tools=get_tool_definitions())
            choice = planning.get("choices", [{}])[0].get("message", {})
            tool_calls = choice.get("tool_calls") or []
            if tool_calls:
                first_call = tool_calls[0]
                function_call = first_call.get("function", {})
                tool_name = function_call.get("name")
                tool_args = json.loads(function_call.get("arguments") or "{}")
                tool_payload = await run_tool_call(tool_name, tool_args)
                yield sse("tool_call", {"tool_call": tool_payload})
                provider_messages.append(choice)
                provider_messages.append({
                    "role": "tool",
                    "tool_call_id": first_call.get("id"),
                    "name": tool_name,
                    "content": tool_payload["output"],
                })
            async for token in stream_provider_tokens(provider, provider_messages, selected_model):
                assistant_text += token
                yield sse("token", {"token": token})

        else:
            provider_messages = build_provider_messages(context, content)
            async for token in stream_provider_tokens(provider, provider_messages, selected_model):
                assistant_text += token
                yield sse("token", {"token": token})

        assistant_message = await create_message(
            db,
            conversation.id,
            MessageRole.ASSISTANT,
            assistant_text,
            model_used=selected_model,
            mode_used=selected_mode,
            tool_calls_json=tool_payload,
            search_sources_json=search_sources,
        )
        latency_ms = int((time.perf_counter() - started_at) * 1000)
        input_tokens = estimate_tokens(content)
        output_tokens = estimate_tokens(assistant_text)
        run = await record_model_run(db, assistant_message.id, selected_model, selected_model, "openrouter", input_tokens, output_tokens, latency_ms, request_id)
        yield sse("done", {"message_id": str(assistant_message.id), "run_id": str(run.id), "request_id": request_id})

    except Exception as exc:
        safe_error = "The model request failed. Check backend logs and provider configuration."
        assistant_text = assistant_text or safe_error
        assistant_message = await create_message(
            db,
            conversation.id,
            MessageRole.ASSISTANT,
            assistant_text,
            model_used=selected_model,
            mode_used=selected_mode,
            tool_calls_json=tool_payload,
            search_sources_json=search_sources,
        )
        latency_ms = int((time.perf_counter() - started_at) * 1000)
        run = await record_model_run(
            db,
            assistant_message.id,
            selected_model,
            selected_model,
            "openrouter",
            estimate_tokens(content),
            estimate_tokens(assistant_text),
            latency_ms,
            request_id,
            status=RunStatus.ERROR,
            fallback_reason=str(exc)[:500],
        )
        yield sse("error", {"message": safe_error, "run_id": str(run.id), "request_id": request_id})
        yield sse("done", {"message_id": str(assistant_message.id), "run_id": str(run.id), "request_id": request_id})
