from app.agents.conversation_agent import ConversationAgent

agent = ConversationAgent()

async def run_conversation(query: str):
    return await agent.run(query)