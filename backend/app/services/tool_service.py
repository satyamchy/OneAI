from app.tools.executor import execute_tool
from app.tools.registry import TOOLS

# Returns OpenAI-compatible tool definitions for the model provider.
def get_tool_definitions() -> list[dict]:
    return TOOLS

# Executes one model-selected tool and returns a serializable result object.
async def run_tool_call(tool_name: str, tool_args: dict) -> dict:
    output = await execute_tool(tool_name, tool_args)
    return {"name": tool_name, "arguments": tool_args, "output": output}
