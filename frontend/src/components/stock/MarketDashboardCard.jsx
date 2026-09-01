import React from 'react';

export default function MarketDashboardCard({ data }) {
  if (!data) return null;

  const { market_status, average_index_change_pct, indices, sectors, top_gainers, top_losers } = data;

  const statusColor = market_status === 'Bullish' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' :
    (market_status === 'Bearish' ? 'bg-rose-500/20 text-rose-400 border-rose-500/40' : 'bg-amber-500/20 text-amber-400 border-amber-500/40');

  return (
    <div className="mb-4 rounded-xl border border-slate-700/60 bg-slate-850 p-4 shadow-lg text-slate-100">
      {/* Market Status Header */}
      <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
        <div className="flex items-center gap-3">
          <span className="text-lg font-bold">Market Condition Dashboard</span>
          <span className={`rounded-full border px-3 py-0.5 text-xs font-semibold ${statusColor}`}>
            ● {market_status} ({average_index_change_pct > 0 ? `+${average_index_change_pct}` : average_index_change_pct}%)
          </span>
        </div>
        <span className="text-xs text-slate-400">Indian Equities (NSE/BSE)</span>
      </div>

      {/* Major Indices Grid */}
      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {indices && indices.map((idx, i) => {
          const isPos = (idx.change_pct || 0) >= 0;
          return (
            <div key={i} className="rounded-lg border border-slate-800 bg-slate-900/80 p-3">
              <div className="text-xs font-medium text-slate-400">{idx.name}</div>
              <div className="mt-1 text-sm font-bold">{idx.current_price ? idx.current_price.toLocaleString() : 'N/A'}</div>
              <div className={`mt-0.5 text-xs font-semibold ${isPos ? 'text-emerald-400' : 'text-rose-400'}`}>
                {isPos ? '▲ +' : '▼ '}{idx.change_pct}%
              </div>
            </div>
          );
        })}
      </div>

      {/* Sectors & Top Gainers/Losers split */}
      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Sector Performance */}
        <div>
          <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">Sector Performance</h4>
          <div className="space-y-2">
            {sectors && sectors.map((sec, i) => {
              const isPos = sec.average_change_pct >= 0;
              return (
                <div key={i} className="flex items-center justify-between rounded bg-slate-900/50 px-3 py-1.5 text-xs">
                  <span className="font-medium">{sec.sector}</span>
                  <span className={`font-semibold ${isPos ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {isPos ? '+' : ''}{sec.average_change_pct}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Top Gainers & Losers */}
        <div className="grid grid-cols-2 gap-2">
          <div>
            <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">Top Gainers</h4>
            <div className="space-y-1.5">
              {top_gainers && top_gainers.map((stk, i) => (
                <div key={i} className="rounded border border-emerald-900/30 bg-emerald-950/20 p-2 text-xs">
                  <div className="font-bold text-slate-200">{stk.symbol}</div>
                  <div className="text-emerald-400">+{stk.change_pct}%</div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-rose-400">Top Losers</h4>
            <div className="space-y-1.5">
              {top_losers && top_losers.map((stk, i) => (
                <div key={i} className="rounded border border-rose-900/30 bg-rose-950/20 p-2 text-xs">
                  <div className="font-bold text-slate-200">{stk.symbol}</div>
                  <div className="text-rose-400">{stk.change_pct}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
