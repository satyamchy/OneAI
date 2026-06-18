function ToolCallBlock({ toolCall }) {
  // Tool calls show the exact tool name, arguments, and raw output for transparency.
  return (
    <details className="mb-3 rounded-lg border border-slate-700 p-3">
      <summary className="cursor-pointer text-sm font-medium text-amber-300">Tool Call: {toolCall.name}</summary>
      <pre className="mt-3 overflow-auto rounded bg-slate-950 p-3 text-xs text-slate-300">{JSON.stringify(toolCall, null, 2)}</pre>
    </details>
  );
}

export default ToolCallBlock;
