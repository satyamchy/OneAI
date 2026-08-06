import asyncio

from app.tools.registry import TOOLS
from app.agents.state import ConversationState


async def tool_executor_node(
    state: ConversationState,
):

    tasks = []

    for step in state["steps"]:

        tool = TOOLS[step.tool]

        tasks.append(

            tool(
                **step.input
            )

        )

    outputs = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    tool_outputs = []

    sources = []

    for output in outputs:

        if isinstance(
            output,
            Exception
        ):
            continue

        tool_outputs.append(output)

        if isinstance(
            output,
            list
        ):
            sources.extend(output)

    return {
        "tool_outputs": tool_outputs,
        "sources": sources
    }