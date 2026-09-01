import React from 'react';

export default function AIPerformanceCard({ performanceData }) {
  if (!performanceData || !performanceData.has_history || !performanceData.history?.length) {
    return null;
  }

  const {
    ticker,
    total_snapshots,
    live_current_price,
    overall_ai_accuracy_score_pct,
    trust_rating,
    history,
  } = performanceData;

  const trustColor = overall_ai_accuracy_score_pct >= 70
    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
    : (overall_ai_accuracy_score_pct >= 50 ? 'bg-amber-500/20 text-amber-400 border-amber-500/40' : 'bg-blue-500/20 text-blue-400 border-blue-500/40');

  return (
    <div className="mt-3 rounded-xl border border-slate-700/60 bg-slate-900/90 p-4 text-slate-100 shadow-md">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            AI Historical Accuracy & Performance Tracking
          </span>
          <span className={`rounded-full border px-2.5 py-0.5 text-[11px] font-semibold ${trustColor}`}>
            ● {trust_rating} ({overall_ai_accuracy_score_pct}%)
          </span>
        </div>
        <span className="text-[11px] text-slate-400">{total_snapshots} Analysis Snapshots</span>
      </div>

      {/* Snapshot History Table */}
      <div className="mt-3 overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/60 uppercase text-slate-400">
            <tr>
              <th className="p-2">Analysis Date</th>
              <th className="p-2">Price at Analysis</th>
              <th className="p-2">Live Price Now</th>
              <th className="p-2">Actual Growth %</th>
              <th className="p-2">AI Signal</th>
              <th className="p-2">Prediction Outcome</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {history.map((h) => {
              const isGain = h.actual_return_pct >= 0;
              return (
                <tr key={h.snapshot_id} className="hover:bg-slate-800/40">
                  <td className="p-2 text-slate-400 font-mono text-[11px]">{h.analyzed_at}</td>
                  <td className="p-2 font-medium">₹{h.initial_price?.toLocaleString()}</td>
                  <td className="p-2 font-semibold text-blue-400">₹{h.current_price?.toLocaleString()}</td>
                  <td className={`p-2 font-bold ${isGain ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {isGain ? '+' : ''}{h.actual_return_pct}%
                  </td>
                  <td className="p-2 font-medium">{h.ai_bias}</td>
                  <td className="p-2">
                    {h.prediction_successful ? (
                      <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-[11px] font-semibold text-emerald-300">
                        ✓ Correct Prediction
                      </span>
                    ) : (
                      <span className="rounded bg-rose-500/20 px-2 py-0.5 text-[11px] font-semibold text-rose-300">
                        ⚠ Diverged
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
