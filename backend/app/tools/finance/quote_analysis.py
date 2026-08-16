import logging

import numpy as np

from app.calculations.finance_calcs import calculate_rsi, calculate_sma, calculate_volatility, calculate_period_return
from app.tools.finance.provider_factory import get_provider

logger = logging.getLogger(__name__)

MANIFEST = {
    "name": "stock_analyzer",
    "description": "Fetch price history and compute technical indicators (SMA, RSI, volatility, return) for a stock ticker.",
    "input_schema": {
        "ticker": "stock ticker symbol, e.g. AAPL",
        "period": "optional lookback window, e.g. '3mo', '6mo', '1y' — defaults to 6mo",
    },
}


async def stock_analyzer(ticker: str, period: str = "6mo") -> dict:
    provider = get_provider()

    try:
        history = await provider.get_historical_prices(ticker, period)
        quote = await provider.get_quote(ticker)
        profile = await provider.get_company_profile(ticker)
    except Exception as e:
        logger.exception("STOCK_ANALYZER_FAILED | ticker=%s period=%s", ticker, period)
        raise RuntimeError(f"stock_analyzer failed for ticker='{ticker}': {e}") from e

    closes = np.array(history["close"])

    indicators = {
        "sma_20": calculate_sma(closes, window=20),
        "sma_50": calculate_sma(closes, window=50),
        "rsi_14": calculate_rsi(closes, window=14),
        "annualized_volatility_pct": calculate_volatility(closes),
        "period_return_pct": calculate_period_return(closes),
    }

    return {
        "ticker": ticker.upper(),
        "name": profile.get("name"),
        "currency": quote.get("currency"),
        "current_price": quote.get("current_price"),
        "52_week_high": quote.get("52_week_high"),
        "52_week_low": quote.get("52_week_low"),
        "pe_ratio": quote.get("pe_ratio"),
        "market_cap": quote.get("market_cap"),
        "recent_closes": history["close"][-5:],
        "indicators": indicators,
        "period_analyzed": period,
        "data_source": "yfinance",
    }
