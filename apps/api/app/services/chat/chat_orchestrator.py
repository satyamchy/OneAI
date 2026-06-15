import time
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import not_found
from app.db.models.user import User
from app.db.repositories.analytics_repository import AnalyticsRepository
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.message_repository import MessageRepository
from app.schemas.message import MessageRead, MessageStreamRequest
from app.services.chains.fallback_chain import FallbackChain
from app.services.chains.message_chain import MessageChain
from app.services.chains.title_chain import TitleChain
from app.services.chat.context_builder import ContextBuilder
from app.services.chat.prompt_builder import PromptBuilder
from app.services.chat.run_recorder import RunRecorder
from app.services.chat.stream_manager import sse_event
from app.services.providers.base_provider import ProviderRequest
from app.services.providers.provider_registry import ProviderRegistry
from app.services.routing.cost_estimator import CostEstimator
from app.services.routing.fallback_policy import FallbackPolicy
from app.services.routing.model_router import ModelRouter, SelectedModel


class ChatOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)
        self.analytics = AnalyticsRepository(db)
        self.context_builder = ContextBuilder(db)
        self.prompt_builder = PromptBuilder()
        self.model_router = ModelRouter(db)
        self.fallback_policy = FallbackPolicy(db)
        self.provider_registry = ProviderRegistry()
        self.run_recorder = RunRecorder(db)
        self.cost_estimator = CostEstimator()
        self.title_chain = TitleChain()

    async def stream_message(
        self,
        *,
        conversation_id: str,
        payload: MessageStreamRequest,
        user: User,
        request_id: str,
    ) -> AsyncIterator[str]:
        started = time.perf_counter()
        conversation = await self.conversations.get_owned(conversation_id, user.id)
        if not conversation:
            raise not_found("Conversation not found")

        user_message = await self.messages.create(
            conversation_id=conversation.id,
            user_id=user.id,
            role="user",
            content=payload.content,
            parent_message_id=payload.parent_message_id,
            metadata_json={"request_id": request_id},
        )
        await self.db.commit()

        selected = await self.model_router.select_model(
            user=user,
            conversation=conversation,
            requested_model_id=payload.model_id,
        )
        run = await self.run_recorder.start(
            request_id=request_id,
            user_id=user.id,
            conversation_id=conversation.id,
            request_message_id=user_message.id,
            provider=selected.provider,
            model_id=selected.model_id,
        )
        await self.db.commit()

        yield sse_event(
            "message_start",
            {
                "request_id": request_id,
                "user_message": MessageRead.model_validate(user_message).model_dump(mode="json"),
                "run": self._run_payload(
                    selected=selected,
                    request_id=request_id,
                    status="started",
                    fallback_used=False,
                    fallback_from_model_id=None,
                    latency_ms=0,
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0,
                    estimated_cost_usd=0,
                ),
            },
        )

        fallback_state = FallbackChain()
        assistant_text = ""
        final_model = selected

        try:
            async for event in self._stream_attempt_events(
                selected=selected,
                payload=payload,
                conversation=conversation,
                request_id=request_id,
            ):
                yield event
            assistant_text = self._last_assistant_text
        except Exception as primary_error:
            assistant_text = getattr(self, "_last_assistant_text", "")
            fallback = await self.fallback_policy.resolve(selected.registry_model)
            if fallback and not assistant_text:
                fallback_state.mark_fallback(selected)
                final_model = fallback
                yield sse_event(
                    "model_fallback",
                    {
                        "request_id": request_id,
                        "from_model_id": selected.model_id,
                        "to_model_id": fallback.model_id,
                        "reason": str(primary_error),
                    },
                )
                try:
                    async for event in self._stream_attempt_events(
                        selected=fallback,
                        payload=payload,
                        conversation=conversation,
                        request_id=request_id,
                    ):
                        yield event
                    assistant_text = self._last_assistant_text
                except Exception as fallback_error:
                    latency_ms = self._latency_ms(started)
                    await self.run_recorder.fail(run, error=fallback_error, latency_ms=latency_ms)
                    await self.analytics.create_event(
                        user_id=user.id,
                        conversation_id=conversation.id,
                        event_name="model_run_failed",
                        event_props_json={"request_id": request_id, "error": str(fallback_error)},
                    )
                    await self.db.commit()
                    yield sse_event(
                        "error",
                        {"request_id": request_id, "message": "Model request failed"},
                    )
                    return
            else:
                latency_ms = self._latency_ms(started)
                await self.run_recorder.fail(run, error=primary_error, latency_ms=latency_ms)
                await self.db.commit()
                yield sse_event(
                    "error",
                    {"request_id": request_id, "message": "Model request failed"},
                )
                return

        assistant_message = await self.messages.create(
            conversation_id=conversation.id,
            user_id=user.id,
            role="assistant",
            content=assistant_text,
            model_id=final_model.model_id,
            provider=final_model.provider,
            model_run_id=run.id,
            parent_message_id=user_message.id,
            metadata_json={
                "request_id": request_id,
                "fallback_used": fallback_state.fallback_used,
            },
        )

        prompt_text = payload.content
        cost = self.cost_estimator.estimate(
            model=final_model.registry_model,
            prompt_text=prompt_text,
            completion_text=assistant_text,
        )
        latency_ms = self._latency_ms(started)
        await self.run_recorder.complete(
            run,
            response_message_id=assistant_message.id,
            provider=final_model.provider,
            model_id=final_model.model_id,
            fallback_used=fallback_state.fallback_used,
            fallback_from_model_id=fallback_state.fallback_from_model_id,
            latency_ms=latency_ms,
            **cost,
        )

        message_count = await self.conversations.message_count(conversation.id)
        if conversation.title == "New Conversation" and message_count <= 2:
            await self.conversations.update(
                conversation,
                title=self.title_chain.generate_title(payload.content),
            )

        await self.analytics.create_event(
            user_id=user.id,
            conversation_id=conversation.id,
            event_name="message_sent",
            event_props_json={
                "request_id": request_id,
                "model_id": final_model.model_id,
                "provider": final_model.provider,
                "fallback_used": fallback_state.fallback_used,
                **cost,
                "latency_ms": latency_ms,
            },
        )
        await self.db.commit()

        yield sse_event(
            "message_done",
            {
                "request_id": request_id,
                "assistant_message": MessageRead.model_validate(assistant_message).model_dump(mode="json"),
                "run": self._run_payload(
                    selected=final_model,
                    request_id=request_id,
                    status="completed",
                    fallback_used=fallback_state.fallback_used,
                    fallback_from_model_id=fallback_state.fallback_from_model_id,
                    latency_ms=latency_ms,
                    **cost,
                ),
            },
        )

    async def _stream_attempt_events(
        self,
        *,
        selected: SelectedModel,
        payload: MessageStreamRequest,
        conversation,
        request_id: str,
        ) -> AsyncIterator[str]:
        self._last_assistant_text = ""
        context_messages = await self.context_builder.build(conversation)
        provider_messages = self.prompt_builder.build(context_messages)
        provider_request = ProviderRequest(
            model_id=selected.model_id,
            messages=provider_messages,
            request_id=request_id,
            temperature=payload.temperature or 0.7,
            max_tokens=payload.max_tokens or 1200,
        )
        chain = MessageChain(self.provider_registry, selected.provider)
        chunks: list[str] = []
        async for chunk in chain.stream(provider_request):
            if chunk.content:
                chunks.append(chunk.content)
                self._last_assistant_text = "".join(chunks)
                yield sse_event(
                    "token",
                    {
                        "request_id": request_id,
                        "content": chunk.content,
                        "model_id": selected.model_id,
                        "provider": selected.provider,
                    },
                )
        self._last_assistant_text = "".join(chunks)

    def _latency_ms(self, started: float) -> int:
        return int((time.perf_counter() - started) * 1000)

    def _run_payload(
        self,
        *,
        selected: SelectedModel,
        request_id: str,
        status: str,
        fallback_used: bool,
        fallback_from_model_id: str | None,
        latency_ms: int,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        estimated_cost_usd: float,
    ) -> dict:
        return {
            "request_id": request_id,
            "provider": selected.provider,
            "model_id": selected.model_id,
            "status": status,
            "fallback_used": fallback_used,
            "fallback_from_model_id": fallback_from_model_id,
            "latency_ms": latency_ms,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": estimated_cost_usd,
        }
