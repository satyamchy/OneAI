from enum import StrEnum

class InteractionMode(StrEnum):
    CHAT = "chat"
    WEB_SEARCH = "web_search"
    TOOLS = "tools"

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class RunStatus(StrEnum):
    SUCCESS = "success"
    FALLBACK = "fallback"
    ERROR = "error"
