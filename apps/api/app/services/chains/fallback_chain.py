from app.services.routing.model_router import SelectedModel


class FallbackChain:
    def __init__(self):
        self.fallback_used = False
        self.fallback_from_model_id: str | None = None

    def mark_fallback(self, from_model: SelectedModel) -> None:
        self.fallback_used = True
        self.fallback_from_model_id = from_model.model_id

