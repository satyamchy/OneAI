from uuid import uuid4

# Generates a short traceable request identifier for API responses and model runs.
def generate_request_id() -> str:
    return f"req_{uuid4().hex}"
