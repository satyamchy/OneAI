import asyncio
import time
import uuid

from app.tools.registry import TOOLS
from app.agents.state import ConversationState
from app.utils.logger import get_logger


logger = get_logger(__name__)


async def execute_tool(step, tool_call_id: str):

    tool_name = step.tool
    tool_input = step.input

    logger.info(
        "TOOL_CALL_START | id=%s | tool=%s | input=%s",
        tool_call_id,
        tool_name,
        tool_input,
    )

    start_time = time.perf_counter()

    try:

        tool = TOOLS.get(tool_name)

        if tool is None:

            logger.error(
                "TOOL_NOT_FOUND | id=%s | tool=%s",
                tool_call_id,
                tool_name,
            )

            return {
                "tool_call_id": tool_call_id,
                "tool": tool_name,
                "input": tool_input,
                "success": False,
                "output": None,
                "error": f"Tool '{tool_name}' not found",
            }

        result = await tool(**tool_input)

        execution_time = round(
            time.perf_counter() - start_time,
            3,
        )

        logger.info(
            "TOOL_CALL_SUCCESS | id=%s | tool=%s | duration=%ss",
            tool_call_id,
            tool_name,
            execution_time,
        )

        logger.debug(
            "TOOL_CALL_OUTPUT | id=%s | tool=%s | output=%s",
            tool_call_id,
            tool_name,
            result,
        )

        return {
            "tool_call_id": tool_call_id,
            "tool": tool_name,
            "input": tool_input,
            "success": True,
            "output": result,
            "execution_time": execution_time,
        }

    except Exception as exc:

        execution_time = round(
            time.perf_counter() - start_time,
            3,
        )

        logger.exception(
            "TOOL_CALL_FAILED | id=%s | tool=%s | duration=%ss",
            tool_call_id,
            tool_name,
            execution_time,
        )

        return {
            "tool_call_id": tool_call_id,
            "tool": tool_name,
            "input": tool_input,
            "success": False,
            "output": None,
            "error": str(exc),
            "execution_time": execution_time,
        }


async def tool_executor_node(
    state: ConversationState,
):

    steps = state.get("steps", [])

    logger.info(
        "TOOL_EXECUTOR_START | tools=%s",
        [step.tool for step in steps],
    )

    tasks = []

    for step in steps:

        tool_call_id = str(uuid.uuid4())

        tasks.append(
            execute_tool(
                step,
                tool_call_id,
            )
        )

    results = await asyncio.gather(*tasks)

    tool_outputs = []
    sources = []

    for result in results:

        tool_outputs.append(result)

        if result["success"]:

            output = result["output"]

            if isinstance(output, list):

                sources.extend(output)

    logger.info(
        "TOOL_EXECUTOR_COMPLETE | executed=%s | successful=%s",
        len(results),
        sum(
            1
            for result in results
            if result["success"]
        ),
    )

    return {
        "tool_outputs": tool_outputs,
        "sources": sources,
    }