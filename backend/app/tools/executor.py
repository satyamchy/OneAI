from app.tools.implementations.calculator import calculate
from app.tools.implementations.current_time import get_current_time
from app.tools.implementations.url_reader import read_url

# Executes a registered tool by name and returns its raw string output.
async def execute_tool(tool_name: str, tool_args: dict) -> str:
    if tool_name == "get_current_time":
        return await get_current_time()
    if tool_name == "calculator":
        return await calculate(tool_args["expression"])
    if tool_name == "url_reader":
        return await read_url(tool_args["url"])
    # TODO Phase 5: gmail_reader, notion_fetcher, and slack_search will be added here.
    raise ValueError(f"Unknown tool: {tool_name}")
