# Generates a simple local fallback title from the first user prompt.
def generate_fallback_title(prompt: str) -> str:
    cleaned = " ".join(prompt.split())
    if len(cleaned) <= 60:
        return cleaned or "New Conversation"
    return f"{cleaned[:57]}..."
