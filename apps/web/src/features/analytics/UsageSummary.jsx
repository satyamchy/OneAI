import { formatCost } from "../../lib/formatCost.js";

export function UsageSummary({ usage }) {
  return (
    <div className="grid grid-cols-4 gap-2 text-sm">
      <span>{usage?.runs || 0} runs</span>
      <span>{usage?.tokens || 0} tokens</span>
      <span>{formatCost(usage?.estimated_cost_usd)}</span>
      <span>{usage?.avg_latency_ms || 0} ms avg</span>
    </div>
  );
}

