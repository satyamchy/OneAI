from langgraph.graph import (
    START,
    END,
    StateGraph
)

from app.agents.state import ConversationState

from app.agents.planner import planner_node
from app.agents.tool_executor import tool_executor_node
from app.agents.answer import answer_node
from app.agents.formatter import formatter_node


def planner_router(
    state: ConversationState,
):

    if state["is_finished"]:
        return "answer"

    return "tool_executor"


def build_graph():

    builder = StateGraph(
        ConversationState
    )

    builder.add_node(
        "planner",
        planner_node
    )

    builder.add_node(
        "tool_executor",
        tool_executor_node
    )

    builder.add_node(
        "answer",
        answer_node
    )

    builder.add_node(
        "formatter",
        formatter_node
    )

    builder.add_edge(
        START,
        "planner"
    )

    builder.add_conditional_edges(

        "planner",

        planner_router,

        {

            "tool_executor": "tool_executor",

            "answer": "answer"

        }

    )

    builder.add_edge(

        "tool_executor",

        "planner"

    )

    builder.add_edge(

        "answer",

        "formatter"

    )

    builder.add_edge(

        "formatter",

        END

    )

    return builder.compile()