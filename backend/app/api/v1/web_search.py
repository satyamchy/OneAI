from app.search.llm import get_llm
from app.search.duckduckgo import web_search_tool
from fastapi import APIRouter
import json

# from app import tools

router = APIRouter(prefix="/search", tags=["web search"])

# llm + web search endpoint
@router.get("/web-search")
def web_search(query: str, max_results: int = 5):

    llm = get_llm()
    search_tool =  web_search_tool()
    # tools = [search_tool]
    search_results =  search_tool.invoke(query)
    prompt = f"""
    User Query: {query}
    Given the search results below, return ONLY a valid JSON array.

    Search Results:
    {search_results}
    """
    
    results = llm.invoke(prompt)
    response_text = results.content.strip()

    if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
           
    # Parse JSON
    try:
        articles = json.loads(response_text)
        return articles
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by LLM",
            "raw_response": response_text
        }
        
# llm endpoint
@router.get("/llm" )
def llm_response(query: str):
     llm = get_llm()
     prompt = f"""
     User Query: {query}
        Given the user query above, return a concise and relevant response.
     """

     results = llm.invoke(prompt)
     return results.content.strip()
   

# llm + agent calling endpoint
@router.get("/llm-agent" )
def llm_response(query: str):
     llm = get_llm()
     prompt = f"""
     User Query: {query}
        Given the user query above, return a concise and relevant response.
     """

     results = llm.invoke(prompt)
     return results.content.strip()


