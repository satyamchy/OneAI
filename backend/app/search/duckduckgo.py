from langchain_community.tools import DuckDuckGoSearchResults

# Calls DuckDuckGo through LangChain and returns normalized source dictionaries.
async def web_search(query: str, max_results: int = 5) -> list[dict]:
    tool = DuckDuckGoSearchResults(output_format="list", num_results=max_results)
    try:
        results = await tool.ainvoke(query)
    except Exception:
        return []
    normalized = []
    for item in results[:max_results]:
        normalized.append({
            "title": item.get("title") or item.get("source") or "Untitled source",
            "url": item.get("link") or item.get("url") or "",
            "snippet": item.get("snippet") or item.get("body") or "",
        })
    return normalized
