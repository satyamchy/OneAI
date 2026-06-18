from app.search.duckduckgo import web_search
from app.search.prompt_builder import build_search_prompt

# Runs web search and formats the results into an LLM-ready prompt.
async def prepare_search_prompt(query: str) -> tuple[str, list[dict]]:
    results = await web_search(query)
    return build_search_prompt(query, results), results
