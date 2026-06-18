const MODE_ICONS = {
  chat: '💬',
  web_search: '🌐',
  tools: '🔧',
};

function ConversationItem({ conversation, active, onSelect }) {
  // Each item shows the conversation title and its current mode icon.
  return (
    <button onClick={onSelect} className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm ${active ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}>
      <span>{MODE_ICONS[conversation.interaction_mode] || '💬'}</span>
      <span className="truncate">{conversation.title}</span>
      <span className="ml-auto hidden text-slate-400 group-hover:inline">×</span>
    </button>
  );
}

export default ConversationItem;
