class TitleChain:
    def generate_title(self, prompt: str) -> str:
        words = [word.strip(".,!?;:()[]{}") for word in prompt.split()]
        title_words = [word for word in words if word][:8]
        if not title_words:
            return "New Conversation"
        title = " ".join(title_words)
        return title[:80]

