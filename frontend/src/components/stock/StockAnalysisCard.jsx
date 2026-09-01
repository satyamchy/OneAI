import React, { useState } from 'react';

export default function StockAnalysisCard({ data }) {
  if (!data || !data.ticker) return null;

  const {
    ticker,
    name,
    currency,
    current_price,
    pe_ratio,
    indicators,
  } = data;

  const [activeTab, setActiveTab] = useState('intraday');

  const rsi = indicators?.rsi_14;
  const sma20 = indicators?.sma_20;
  const sma50 = indicators?.sma_50;
  const macd = indicators?.macd;
  const pivots = indicators?.pivot_points;
  const vol = indicators?.annualized_volatility_pct;
  const drawdown = indicators?.max_drawdown_pct;

  const rsiBadge = rsi ? (
    rsi > 70 ? 'bg-rose-500/20 text-rose-400 border-rose-500/40' :
    (rsi < 30 ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' : 'bg-blue-500/20 text-blue-400 border-blue-500/40')
  ) : '';

  return (
    <div className="mb-4 rounded-xl border border-slate-700/60 bg-slate-850 p-4 shadow-lg text-slate-100">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700/60 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl font-black text-blue-400">{ticker}</span>
            <span className="text-xs text-slate-400">{name}</span>
          </div>
          <div className="mt-1 flex items-baseline gap-2">
            <span className="text-2xl font-bold">{currency === 'INR' ? '₹' : '$'}{current_price?.toLocaleString()}</span>
            {pe_ratio && <span className="text-xs text-slate-400">P/E: {pe_ratio}</span>}
          </div>
        </div>

        {/* Quick Badges */}
        <div className="flex flex-wrap gap-2 text-xs">
          {rsi && (
            <span className={`rounded-full border px-2.5 py-1 font-semibold ${rsiBadge}`}>
              RSI (14): {rsi}
            </span>
          )}
          {vol && (
            <span className="rounded-full border border-slate-600 bg-slate-800 px-2.5 py-1 font-medium text-slate-300">
              Volatility: {vol}%
            </span>
          )}
          {drawdown && (
            <span className="rounded-full border border-slate-600 bg-slate-800 px-2.5 py-1 font-medium text-amber-400">
              Max Drawdown: {drawdown}%
            </span>
          )}
        </div>
      </div>

      {/* Indicators Summary Row */}
      <div className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
        <div className="rounded bg-slate-900/60 p-2">
          <span className="text-slate-400">SMA (20):</span>
          <div className="font-semibold text-slate-200">{sma20 ? `${currency === 'INR' ? '₹' : '$'}${sma20}` : 'N/A'}</div>
        </div>
        <div className="rounded bg-slate-900/60 p-2">
          <span className="text-slate-400">SMA (50):</span>
          <div className="font-semibold text-slate-200">{sma50 ? `${currency === 'INR' ? '₹' : '$'}${sma50}` : 'N/A'}</div>
        </div>
        <div className="rounded bg-slate-900/60 p-2">
          <span className="text-slate-400">MACD Histogram:</span>
          <div className={`font-semibold ${(macd?.histogram || 0) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {macd?.histogram !== undefined ? macd.histogram : 'N/A'}
          </div>
        </div>
        <div className="rounded bg-slate-900/60 p-2">
          <span className="text-slate-400">Pivot Level:</span>
          <div className="font-semibold text-blue-400">{pivots?.pivot ? `${currency === 'INR' ? '₹' : '$'}${pivots.pivot}` : 'N/A'}</div>
        </div>
      </div>

      {/* Support & Resistance Bar */}
      {pivots && (
        <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900/90 p-3 text-xs">
          <div className="mb-1 text-xs font-semibold text-slate-400">Key Levels (Pivot Points)</div>
          <div className="flex flex-wrap items-center justify-between gap-1 text-slate-300">
            <span className="text-rose-400">R2: ₹{pivots.r2}</span>
            <span className="text-rose-300">R1: ₹{pivots.r1}</span>
            <span className="font-bold text-blue-400">P: ₹{pivots.pivot}</span>
            <span className="text-emerald-300">S1: ₹{pivots.s1}</span>
            <span className="text-emerald-400">S2: ₹{pivots.s2}</span>
          </div>
        </div>
      )}
    </div>
  );
}
