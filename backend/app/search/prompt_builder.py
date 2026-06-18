# Formats search results into a source-grounded prompt for the LLM.
def build_search_prompt(query: str, results: list[dict]) -> str:
    sources = "\n".join(
        f"[{index}] {item.get('title')}\nURL: {item.get('url')}\nSnippet: {item.get('snippet')}"
        for index, item in enumerate(results, start=1)
    )
    return (
        "Answer the question using only the search results below when possible. "
        "Cite source numbers where relevant.\n\n"
        f"Search Results:\n{sources or 'No search results found.'}\n\n"
        f"Question: {query}"
    )
