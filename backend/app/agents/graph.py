from langgraph.graph import (START, END, StateGraph )

from app.agents.state import ConversationState
from app.agents.planner import planner_node
from app.agents.router import router_node
from app.agents.company_resolver_node import company_resolver_node
from app.agents.tool_executor import tool_executor_node
from app.agents.answer import answer_node
from app.agents.formatter import formatter_node

MAX_LOOPS = 4  # hard safety cap: planner<->tool_executor round trips

def planner_router(
    state: ConversationState,
):
    # Safety net: never trust the LLM's is_finished flag alone to
    # prevent runaway loops.
    if state.get("loop_count", 0) >= MAX_LOOPS:
        return "answer"

    # If the LLM says it's done, respect that.
    if state["is_finished"]:
        return "answer"

    # If the planner requested no tools at all, there's nothing left
    # to execute — go straight to answer instead of bouncing through
    # an empty tool_executor round trip.
    if not state.get("steps"):
        return "answer"

    return "tool_executor"


def build_graph():

    builder = StateGraph(
        ConversationState
    )

    builder.add_node("router", router_node)
    builder.add_node("company_resolver", company_resolver_node)
    builder.add_node("planner", planner_node)
    builder.add_node("tool_executor", tool_executor_node)
    builder.add_node("answer", answer_node)
    builder.add_node("formatter", formatter_node)

    builder.add_edge(START, "router")
    builder.add_edge("router", "company_resolver")
    builder.add_edge("company_resolver", "planner")

    builder.add_conditional_edges(
        "planner",
        planner_router,
        {
            "tool_executor": "tool_executor",
            "answer": "answer",
        },
    )

    builder.add_edge("tool_executor", "planner")
    builder.add_edge("answer", "formatter")
    builder.add_edge("formatter", END)
    
    return builder.compile()