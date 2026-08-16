"""
Deterministic financial calculations. Pure functions, no LLM calls,
no network calls, no side effects. Every function here must be unit
tested (see tests/calculations/test_finance_calcs.py) and must return
None rather than a fabricated number when there isn't enough data.
"""

import numpy as np


def _clean(x) -> float | None:
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return None
    return round(float(x), 2)


def calculate_sma(closes: np.ndarray, window: int) -> float | None:
    if len(closes) < window:
        return None
    return _clean(np.mean(closes[-window:]))


def calculate_rsi(closes: np.ndarray, window: int = 14) -> float | None:
    if len(closes) < window + 1:
        return None
    deltas = np.diff(closes)
    gains = np.clip(deltas, 0, None)
    losses = -np.clip(deltas, None, 0)
    avg_gain = np.mean(gains[-window:])
    avg_loss = np.mean(losses[-window:])
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return _clean(100 - (100 / (1 + rs)))


def calculate_volatility(closes: np.ndarray) -> float | None:
    """Annualized volatility (%) from daily closes."""
    if len(closes) < 2:
        return None
    returns = np.diff(closes) / closes[:-1]
    return _clean(np.std(returns) * np.sqrt(252) * 100)


def calculate_period_return(closes: np.ndarray) -> float | None:
    if len(closes) < 2 or closes[0] == 0:
        return None
    return _clean((closes[-1] / closes[0] - 1) * 100)


def calculate_cagr(begin_value: float, end_value: float, years: float) -> float | None:
    if begin_value is None or end_value is None or years <= 0 or begin_value <= 0:
        return None
    return _clean(((end_value / begin_value) ** (1 / years) - 1) * 100)


def calculate_pe(price: float | None, eps: float | None) -> float | None:
    if price is None or eps is None or eps == 0:
        return None
    return _clean(price / eps)


def calculate_debt_to_equity(total_debt: float | None, shareholders_equity: float | None) -> float | None:
    if total_debt is None or shareholders_equity is None or shareholders_equity == 0:
        return None
    return _clean(total_debt / shareholders_equity)


def calculate_roe(net_income: float | None, shareholders_equity: float | None) -> float | None:
    if net_income is None or shareholders_equity is None or shareholders_equity == 0:
        return None
    return _clean((net_income / shareholders_equity) * 100)


def calculate_net_margin(net_income: float | None, revenue: float | None) -> float | None:
    if net_income is None or revenue is None or revenue == 0:
        return None
    return _clean((net_income / revenue) * 100)


def calculate_drawdown(closes: np.ndarray) -> float | None:
    """Maximum drawdown (%) over the given closes series."""
    if len(closes) < 2:
        return None
    running_max = np.maximum.accumulate(closes)
    drawdowns = (closes - running_max) / running_max
    return _clean(np.min(drawdowns) * 100)
