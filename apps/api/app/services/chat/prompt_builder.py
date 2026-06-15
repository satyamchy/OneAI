from app.services.providers.base_provider import ProviderMessage


class PromptBuilder:
    def build(self, messages: list[ProviderMessage]) -> list[ProviderMessage]:
        system_message = ProviderMessage(
            role="system",
            content=(
                "You are OneAI, a helpful personal AI assistant. "
                "Answer clearly, preserve useful context, and format code carefully. "
                "You do not have memory, RAG, tools, or web search enabled in Phase 1."
            ),
        )
        return [system_message, *messages]

