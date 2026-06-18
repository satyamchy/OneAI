# Estimates model cost from per-token pricing values stored in the model registry.
def estimate_cost(input_tokens: int, output_tokens: int, input_cost: float = 0.0, output_cost: float = 0.0) -> float:
    return (input_tokens * input_cost) + (output_tokens * output_cost)
