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
        tasks.append(execute_tool(step, tool_call_id))

    results = await asyncio.gather(*tasks)

    tool_outputs = []
    sources = []

    # Dedupe against URLs already seen in this batch AND in prior
    # rounds (state["sources"] holds everything accumulated so far).
    seen_urls = {
        source.get("url")
        for source in state.get("sources", [])
        if source.get("url")
    }

    for result in results:

        tool_outputs.append(result)

        if result["success"]:

            output = result["output"]

            if isinstance(output, list):

                for item in output:
                    url = item.get("url") if isinstance(item, dict) else None

                    if url and url in seen_urls:
                        continue  # already have this source

                    if url:
                        seen_urls.add(url)

                    sources.append(item)

            elif isinstance(output, dict):
                # Structured data (e.g. stock_analyzer) — no URL to dedupe
                # against, so wrap it with a synthetic key based on tool +
                # ticker/query so a repeated identical call doesn't duplicate.
                synthetic_key = f"internal://{result['tool']}/{tool_input.get('ticker') or tool_input.get('query', '')}" if (tool_input := result.get("input")) else f"internal://{result['tool']}"

                if synthetic_key in seen_urls:
                    continue

                seen_urls.add(synthetic_key)
                sources.append({
                    "source_type": "structured_data",
                    "tool": result["tool"],
                    "url": synthetic_key,
                    "data": output,
                })

    logger.info(
        "TOOL_EXECUTOR_COMPLETE | executed=%s | successful=%s | new_sources=%s",
        len(results),
        sum(1 for result in results if result["success"]),
        len(sources),
    )

    return {
        "tool_outputs": tool_outputs,
        "sources": sources,
    }