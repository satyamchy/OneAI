"""
Resolves free-text company references ("Apple", "AAPL", "TCS", "Reliance") to a
canonical CompanyEntity. Deterministic first (alias table + ticker
validation against the provider), not LLM-only — per section 5's
requirement not to rely solely on an LLM for ticker resolution.
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
    "nifty": "^NSEI",
    "nifty 50": "^NSEI",
    "nifty50": "^NSEI",
    "sensex": "^BSESN",
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "tata consultancy services": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "hcl tech": "HCLTECH.NS",
    "hcltech": "HCLTECH.NS",
    "wipro": "WIPRO.NS",
    "hdfc": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfcbank": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icicibank": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
    "state bank of india": "SBIN.NS",
    "sbin": "SBIN.NS",
    "tata motors": "TATAMOTORS.NS",
    "tatamotors": "TATAMOTORS.NS",
    "tata steel": "TATASTEEL.NS",
    "tatasteel": "TATASTEEL.NS",
    "maruti": "MARUTI.NS",
    "maruti suzuki": "MARUTI.NS",
    "lt": "LT.NS",
    "l&t": "LT.NS",
    "larsen & toubro": "LT.NS",
    "axis bank": "AXISBANK.NS",
    "axisbank": "AXISBANK.NS",
    "sun pharma": "SUNPHARMA.NS",
    "sunpharma": "SUNPHARMA.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "bajfinance": "BAJFINANCE.NS",
    "itc": "ITC.NS",
    "kotak": "KOTAKBANK.NS",
    "kotak bank": "KOTAKBANK.NS",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
}


class CompanyResolutionError(Exception):
    pass


async def resolve_company(text: str) -> CompanyEntity:
    raw = text.strip()
    key = raw.lower()
    
    if key in COMMON_ALIASES:
        candidate = COMMON_ALIASES[key]
    else:
        if "." in raw or "^" in raw:
            candidate = raw.upper()
        else:
            candidate = f"{raw.upper()}.NS"

    provider = get_provider()
    profile = {}
    try:
        profile = await provider.get_company_profile(candidate)
    except Exception as e:
        if candidate.endswith(".NS"):
            try:
                candidate_raw = candidate[:-3]
                profile = await provider.get_company_profile(candidate_raw)
                candidate = candidate_raw
            except Exception:
                raise CompanyResolutionError(
                    f"Could not resolve '{text}' to a valid ticker: {e}"
                ) from e
        else:
            raise CompanyResolutionError(
                f"Could not resolve '{text}' to a valid ticker: {e}"
            ) from e

    if not profile.get("name"):
        # Fallback profile if profile name missing
        profile["name"] = candidate

    return CompanyEntity(
        name=profile["name"],
        ticker=profile.get("ticker", candidate),
        exchange=profile.get("exchange"),
        country=profile.get("country"),
        sector=profile.get("sector"),
        industry=profile.get("industry"),
    )


async def resolve_companies(texts: list[str]) -> list[CompanyEntity]:
    """For comparison queries — resolves each independently."""
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
