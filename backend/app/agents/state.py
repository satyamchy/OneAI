from typing import Annotated, Any

from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from app.schemas.planner import ToolStep


class ConversationState(TypedDict):

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Original query
    query: str

    # Planner output
    steps: list[ToolStep]

    # Outputs returned from tools
    tool_outputs: list[Any]

    # Unified sources from all tools
    sources: list[dict]

    # Context built from sources
    context: str

    # Final answer
    answer: str

    # Planner decision
    is_finished: bool

    # Error
    error: str