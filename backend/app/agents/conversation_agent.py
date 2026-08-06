from app.agents.graph import build_graph
from app.agents.state import ConversationState


class ConversationAgent:

    def __init__(self):

        self.graph = build_graph()

    async def run(
        self,
        query: str,
    ):

        initial_state: ConversationState = {

            "messages": [],

            "query": query,

            "steps": [],

            "tool_outputs": [],

            "sources": [],

            "context": "",

            "answer": "",

            "is_finished": False,

            "error": ""

        }

        return await self.graph.ainvoke(
            initial_state
        )