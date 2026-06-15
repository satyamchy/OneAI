from app.db.models.model_registry import ModelRegistry


def estimate_tokens(text: str) -> int:
    return max(1, int(len(text) / 4))


class CostEstimator:
    def estimate(
        self,
        *,
        model: ModelRegistry,
        prompt_text: str,
        completion_text: str,
    ) -> dict[str, int | float]:
        prompt_tokens = estimate_tokens(prompt_text)
        completion_tokens = estimate_tokens(completion_text)
        total_tokens = prompt_tokens + completion_tokens
        cost = (
            prompt_tokens * model.input_cost_per_1m / 1_000_000
            + completion_tokens * model.output_cost_per_1m / 1_000_000
        )
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(float(cost), 8),
        }

