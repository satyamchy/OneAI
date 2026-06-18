from datetime import datetime, timezone

# Returns the current UTC date and time as an ISO 8601 string.
async def get_current_time() -> str:
    return datetime.now(timezone.utc).isoformat()
