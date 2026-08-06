from app.agents.state import ConversationState


async def formatter_node(
    state: ConversationState,
):

    answer = (state.get("answer") or "").strip()

    if not answer:
        answer = "Sorry, I couldn't generate an answer."

    return {
        "answer": answer,
        "sources": state.get("sources", []),
        "error": state.get("error", "")
    }