import logging
from langchain_community.tools import DuckDuckGoSearchResults

logger = logging.getLogger(__name__)


async def web_search(
    query: str,
    max_results: int = 5,
) -> list[dict]:

    tool = DuckDuckGoSearchResults(
        output_format="list",
        num_results=max_results,
    )

    try:

        results = await tool.ainvoke(query)

    except Exception as e:

        logger.exception(e)

        return []

    normalized = []

    for item in results[:max_results]:

        normalized.append(

            {
                "title": item.get("title")
                or item.get("source")
                or "Untitled",

                "url": item.get("link")
                or item.get("url")
                or "",

                "snippet": item.get("snippet")
                or item.get("body")
                or "",
            }

        )

    return normalized