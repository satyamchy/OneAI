import { useEffect, useState } from 'react';
import { createConversation, listConversations, updateConversation } from '../api/conversationApi.js';
import { listMessages } from '../api/messageApi.js';
import Sidebar from '../components/sidebar/Sidebar.jsx';
import ModeSelector from '../components/mode/ModeSelector.jsx';
import ChatArea from '../components/chat/ChatArea.jsx';
import Composer from '../components/chat/Composer.jsx';
import RunDetailsPanel from '../components/run-details/RunDetailsPanel.jsx';

const GUEST_CONVERSATION = {
  id: 'guest-conversation',
  title: 'Guest Exploration',
  selected_model: 'openai/gpt-4o-mini',
  interaction_mode: 'chat',
};

function ChatPage() {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [runDetails, setRunDetails] = useState(null);
  const isGuest = localStorage.getItem('paios_token') === 'guest';

  // Loads conversations from the API, or creates a local guest workspace for exploration.
  useEffect(() => {
    async function load() {
      if (isGuest) {
        setConversations([GUEST_CONVERSATION]);
        setActiveConversation(GUEST_CONVERSATION);
        return;
      }
      const data = await listConversations();
      if (data.conversations.length) {
        setConversations(data.conversations);
        setActiveConversation(data.conversations[0]);
      } else {
        const created = await createConversation();
        setConversations([created.conversation]);
        setActiveConversation(created.conversation);
      }
    }
    load();
  }, [isGuest]);

  // Loads messages when the active conversation changes, with local sample data for guest mode.
  useEffect(() => {
    if (!activeConversation) return;
    if (isGuest) {
      setMessages([{ id: 'guest-welcome', role: 'assistant', content: 'You are exploring PAIOS without login. Messages stay in this browser session and do not call the backend.' }]);
      return;
    }
    listMessages(activeConversation.id).then((data) => setMessages(data.messages));
  }, [activeConversation?.id, isGuest]);

  // Updates the mode on the server, or locally for guest exploration.
  async function handleModeChange(mode) {
    if (isGuest) {
      const updated = { ...activeConversation, interaction_mode: mode };
      setActiveConversation(updated);
      setConversations([updated]);
      return;
    }
    const data = await updateConversation(activeConversation.id, { interaction_mode: mode });
    setActiveConversation(data.conversation);
    setConversations((items) => items.map((item) => item.id === data.conversation.id ? data.conversation : item));
  }

  return (
    <main className="grid h-screen grid-cols-[280px_1fr_320px] bg-slate-950 text-slate-100">
      <Sidebar conversations={conversations} activeConversation={activeConversation} onSelect={setActiveConversation} />
      <section className="flex min-w-0 flex-col border-x border-slate-800">
        {activeConversation && <ModeSelector mode={activeConversation.interaction_mode} onChange={handleModeChange} />}
        <ChatArea messages={messages} />
        {activeConversation && <Composer conversation={activeConversation} messages={messages} setMessages={setMessages} setRunDetails={setRunDetails} />}
      </section>
      <RunDetailsPanel details={runDetails} />
    </main>
  );
}

export default ChatPage;
