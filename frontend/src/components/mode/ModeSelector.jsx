const MODES = [
  { value: 'web_search', label: '🌐 Web Search', title: 'Stateless web search with sources.' },
  { value: 'chat', label: '💬 Chat', title: 'Standard conversation with recent history.' },
  { value: 'tools', label: '🔧 tools', title: 'Let the model call registered local tools.' },
];

function ModeSelector({ mode, onChange }) {
  // Mode changes are persisted per conversation and affect only the next message.
  return (
    <div className="flex justify-center border-b border-slate-800 bg-slate-950 p-3">
      <div className="rounded-xl bg-slate-900 p-1">
        {MODES.map((item) => (
          <button key={item.value} title={item.title} onClick={() => onChange(item.value)} className={`rounded-lg px-4 py-2 text-sm ${mode === item.value ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}>
            {item.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ModeSelector;
