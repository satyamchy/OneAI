import ConversationItem from './ConversationItem.jsx';

function Sidebar({ conversations, activeConversation, onSelect }) {
  // The sidebar keeps conversation navigation separate from chat rendering.
  return (
    <aside className="flex h-screen flex-col bg-slate-900 p-4">
      <h1 className="text-xl font-semibold text-white">PAIOS</h1>
      <div className="mt-6 space-y-2 overflow-y-auto">
        {conversations.map((conversation) => (
          <ConversationItem key={conversation.id} conversation={conversation} active={conversation.id === activeConversation?.id} onSelect={() => onSelect(conversation)} />
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;
