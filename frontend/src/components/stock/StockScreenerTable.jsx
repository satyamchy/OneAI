import React from 'react';

export default function StockScreenerTable({ data }) {
  if (!data || !data.ranked_stocks) return null;

  const { screening_criteria, ranked_stocks } = data;

  return (
    <div className="mb-4 overflow-hidden rounded-xl border border-slate-700/60 bg-slate-850 shadow-lg text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-700/60 p-4">
        <div>
          <h3 className="text-sm font-bold capitalize">AI Stock Screener Rankings</h3>
          <p className="text-xs text-slate-400">Criteria: <span className="font-semibold text-blue-400 capitalize">{screening_criteria}</span></p>
        </div>
        <span className="rounded bg-blue-500/20 px-2 py-1 text-xs font-semibold text-blue-300">
          Top {ranked_stocks.length} Selected
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 uppercase text-slate-400">
            <tr>
              <th className="p-3">Rank</th>
              <th className="p-3">Stock</th>
              <th className="p-3">Price</th>
              <th className="p-3">Trend</th>
              <th className="p-3">RSI (14)</th>
              <th className="p-3">Risk Level</th>
              <th className="p-3">Signal Rationale</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {ranked_stocks.map((stk) => {
              const isBull = stk.trend.includes('Bullish');
              const riskBadge = stk.risk_level === 'High' ? 'bg-rose-500/20 text-rose-400' :
                (stk.risk_level === 'Medium' ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400');
              
              return (
                <tr key={stk.rank} className="hover:bg-slate-800/40">
                  <td className="p-3 font-bold text-blue-400">#{stk.rank}</td>
                  <td className="p-3 font-semibold">
                    <div>{stk.symbol}</div>
                    <div className="text-[10px] text-slate-400 font-normal">{stk.name}</div>
                  </td>
                  <td className="p-3 font-medium">₹{stk.current_price?.toLocaleString()}</td>
                  <td className={`p-3 font-medium ${isBull ? 'text-emerald-400' : 'text-slate-300'}`}>{stk.trend}</td>
                  <td className="p-3">{stk.rsi_14 ?? 'N/A'}</td>
                  <td className="p-3">
                    <span className={`rounded-full px-2 py-0.5 font-semibold ${riskBadge}`}>
                      {stk.risk_level}
                    </span>
                  </td>
                  <td className="p-3 text-slate-300 max-w-xs truncate">{stk.signal_summary}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
