from langchain_core.prompts import ChatPromptTemplate

from app.schemas.planner import PlannerResponse
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.llm.groq import get_llm
from app.agents.state import ConversationState
from app.utils.logger import get_logger

logger = get_logger(__name__)

llm = get_llm()

planner_llm = llm.with_structured_output(
    PlannerResponse,
        method="json_mode"
)

planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNER_PROMPT),
        (
            "human",
            """
Question:
{query}

Previous Tool Outputs:
{tool_outputs}
"""
        ),
    ]
)


async def planner_node(
    state: ConversationState,
):

    chain = planner_prompt | planner_llm

    response = await chain.ainvoke(

        {

            "query": state["query"],

            "tool_outputs": state["tool_outputs"]

        }

    )

     # Log planner's decision
    logger.info(
        "PLANNER_DECISION | query=%s | tools=%s | finished=%s | reason=%s",
        state["query"],
        [step.tool for step in response.steps],
        response.is_finished,
        response.reason,
    )

    return {
        "steps": response.steps,
        "is_finished": response.is_finished
    }