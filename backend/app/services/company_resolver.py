"""
Resolves free-text company references ("Apple", "AAPL", "Apple Inc") to a
canonical CompanyEntity. Deterministic first (alias table + ticker
validation against the provider), not LLM-only — per section 5's
requirement not to rely solely on an LLM for ticker resolution.

This is a starting alias table, not a full company database — expand
COMMON_ALIASES as real queries reveal gaps, or swap in a proper
symbol-search API later (one function to change, not the whole resolver).
"""

from app.schemas.finance.company import CompanyEntity
from app.tools.finance.provider_factory import get_provider

COMMON_ALIASES = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
}


class CompanyResolutionError(Exception):
    pass


async def resolve_company(text: str) -> CompanyEntity:
    candidate = COMMON_ALIASES.get(text.strip().lower(), text.strip().upper())

    provider = get_provider()
    try:
        profile = await provider.get_company_profile(candidate)
    except Exception as e:
        raise CompanyResolutionError(
            f"Could not resolve '{text}' to a valid ticker: {e}"
        ) from e

    if not profile.get("name"):
        raise CompanyResolutionError(f"'{text}' did not resolve to a recognizable company.")

    return CompanyEntity(
        name=profile["name"],
        ticker=profile["ticker"],
        exchange=profile.get("exchange"),
        country=profile.get("country"),
        sector=profile.get("sector"),
        industry=profile.get("industry"),
    )


async def resolve_companies(texts: list[str]) -> list[CompanyEntity]:
    """For comparison queries — resolves each independently, collects
    failures instead of letting one bad ticker kill the whole comparison."""
    entities = []
    errors = []
    for text in texts:
        try:
            entities.append(await resolve_company(text))
        except CompanyResolutionError as e:
            errors.append(str(e))
    if errors and not entities:
        raise CompanyResolutionError("; ".join(errors))
    return entities
