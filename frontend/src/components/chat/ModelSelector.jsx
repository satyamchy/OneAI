const DEFAULT_MODELS = [
  'openai/gpt-4o-mini',
  'anthropic/claude-3.5-sonnet',
  'google/gemini-flash-1.5',
  'meta-llama/llama-3.1-70b-instruct',
];

function ModelSelector({ value, onChange }) {
  // The compact selector chooses the model for the next streamed message.
  return (
    <select value={value} onChange={(event) => onChange(event.target.value)} className="max-w-48 rounded-lg bg-slate-800 p-2 text-xs text-white">
      {DEFAULT_MODELS.map((model) => <option key={model} value={model}>{model}</option>)}
    </select>
  );
}

export default ModelSelector;
