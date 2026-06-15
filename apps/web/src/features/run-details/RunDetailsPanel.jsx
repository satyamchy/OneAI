import { Activity, Clock, Coins, Cpu, Fingerprint, GitBranch, Hash } from "lucide-react";

import { formatCost } from "../../lib/formatCost.js";

function DetailRow({ icon: Icon, label, value }) {
  return (
    <div className="flex items-start gap-3 rounded-md border border-stone-200 bg-stone-50 px-3 py-2">
      <Icon className="mt-0.5 text-emerald-700" size={16} />
      <div className="min-w-0">
        <div className="text-xs font-medium uppercase tracking-wide text-stone-500">{label}</div>
        <div className="truncate text-sm font-medium text-stone-950">{value || "-"}</div>
      </div>
    </div>
  );
}

export function RunDetailsPanel({ run, usage }) {
  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-stone-200 p-4">
        <h2 className="text-sm font-semibold text-stone-950">Run Details</h2>
        <p className="mt-1 text-xs text-stone-500">Live model metadata for the latest response.</p>
      </div>

      <div className="scrollbar-thin flex-1 space-y-3 overflow-y-auto p-4">
        <DetailRow icon={Cpu} label="Model" value={run?.model_id} />
        <DetailRow icon={Activity} label="Provider" value={run?.provider} />
        <DetailRow icon={Clock} label="Latency" value={run ? `${run.latency_ms || 0} ms` : "-"} />
        <DetailRow icon={Hash} label="Tokens" value={run ? `${run.total_tokens || 0}` : "-"} />
        <DetailRow icon={Coins} label="Cost" value={formatCost(run?.estimated_cost_usd)} />
        <DetailRow icon={GitBranch} label="Fallback" value={run?.fallback_used ? "Used" : "No"} />
        <DetailRow icon={Fingerprint} label="Request" value={run?.request_id} />

        <div className="rounded-lg border border-stone-200 bg-white p-4 shadow-panel">
          <div className="text-xs font-medium uppercase tracking-wide text-stone-500">Usage</div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div>
              <div className="text-stone-500">Runs</div>
              <div className="font-semibold text-stone-950">{usage?.runs || 0}</div>
            </div>
            <div>
              <div className="text-stone-500">Tokens</div>
              <div className="font-semibold text-stone-950">{usage?.tokens || 0}</div>
            </div>
            <div>
              <div className="text-stone-500">Cost</div>
              <div className="font-semibold text-stone-950">
                {formatCost(usage?.estimated_cost_usd)}
              </div>
            </div>
            <div>
              <div className="text-stone-500">Avg latency</div>
              <div className="font-semibold text-stone-950">{usage?.avg_latency_ms || 0} ms</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

