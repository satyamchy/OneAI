from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.core.constants import MessageRole

# Converts database messages into OpenRouter-compatible chat message dictionaries.
def build_provider_messages(messages, latest_user_prompt: str | None = None) -> list[dict]:
    provider_messages = []
    for message in messages:
        if message.role == MessageRole.USER:
            lc_message = HumanMessage(content=message.content)
            role = "user"
        elif message.role == MessageRole.ASSISTANT:
            lc_message = AIMessage(content=message.content)
            role = "assistant"
        else:
            lc_message = SystemMessage(content=message.content)
            role = "system"
        provider_messages.append({"role": role, "content": lc_message.content})
    if latest_user_prompt:
        provider_messages.append({"role": "user", "content": latest_user_prompt})
    return provider_messages
