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

      # response is AIMessage
    logger.info(
        "RAW_PLANNER_RESPONSE | %s",
        response.content
    )

    # Convert JSON string -> PlannerResponse
    planner_response = PlannerResponse.model_validate_json(
        response.content
    )
     # Log planner's decision
    # logger.info(
    #     "PLANNER_DECISION | query=%s | tools=%s | finished=%s | reason=%s",
    #     state["query"],
    #     [step.tool for step in response.steps],
    #     response.is_finished,
    #     response.reason,
    # )
    logger.info(
        "PLANNER_DECISION | query=%s | tools=%s | finished=%s | reason=%s",
        state["query"],
        [step.tool for step in planner_response.steps],
        planner_response.is_finished,
        planner_response.reason,
    )

    return {
        "steps": planner_response.steps,
        "is_finished": planner_response.is_finished
    }