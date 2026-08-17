from langchain_core.prompts import ChatPromptTemplate

from app.schemas.planner import PlannerResponse
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.llm.groq import get_llm
from app.agents.state import ConversationState
from app.utils.logger import get_logger

logger = get_logger(__name__)

llm = get_llm()

# planner_llm = llm.with_structured_output(
#     PlannerResponse,
#         method="json_mode"
# )
planner_llm = llm.bind(
    response_format={"type": "json_object"}
)

planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNER_PROMPT),
        (
            "human",
            """
Question:
{query}

Resolved Companies (use these exact tickers if the question is about one of them — do not guess a different ticker):
{companies}

Previous Tool Outputs:
{tool_outputs}
"""
        ),
    ]
)

def _already_searched(query: str, tool_outputs: list) -> bool:
    normalized = query.strip().lower()
    for output in tool_outputs:
        prior_input = output.get("input", {})
        prior_query = str(prior_input.get("query", "")).strip().lower()
        if prior_query and prior_query == normalized:
            return True
    return False


async def planner_node(
    state: ConversationState,
):

    chain = planner_prompt | planner_llm

    companies = state.get("companies", [])
    companies_text = (
        "\n".join(f"- {c['name']} -> ticker: {c['ticker']}" for c in companies)
        if companies
        else "None resolved."
    )

    response = await chain.ainvoke(
        {
            "query": state["query"],
            "companies": companies_text,
            "tool_outputs": state["tool_outputs"]
        }
    )

    # response is AIMessage
    logger.info("RAW_PLANNER_RESPONSE | %s", response.content)

    # Convert JSON string -> PlannerResponse
    planner_response = PlannerResponse.model_validate_json(
        response.content
    )

    # Guard against the model contradicting itself: if it explicitly
    # says the answer is already known but forgot to flip
    # is_finished, force it.
    reason_lower = planner_response.reason.lower()
    if not planner_response.is_finished and (
        "already known" in reason_lower
        or "already have" in reason_lower
        or "already answered" in reason_lower
    ):
        planner_response.is_finished = True
        planner_response.steps = []

    # Drop any step that repeats a query we've already run — avoids
    # firing the same web_search call over and over.
    deduped_steps = [
        step
        for step in planner_response.steps
        if not (
            step.tool == "web_search"
            and _already_searched(
                step.input.get("query", ""),
                state.get("tool_outputs", []),
            )
        )
    ]

    if not deduped_steps and planner_response.steps:
        # Every requested step was a duplicate — nothing new to do.
        planner_response.is_finished = True


    logger.info(
        "PLANNER_DECISION | query=%s | tools=%s | finished=%s | reason=%s",
        state["query"],
        [step.tool for step in deduped_steps],
        planner_response.is_finished,
        planner_response.reason,
    )

    return {
        "steps": deduped_steps,
        "is_finished": planner_response.is_finished,
        "loop_count": state.get("loop_count", 0) + 1,
    }