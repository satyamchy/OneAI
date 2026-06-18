import { useState } from 'react';
import { streamMessage } from '../../api/messageApi.js';
import ModelSelector from './ModelSelector.jsx';

function Composer({ conversation, messages, setMessages, setRunDetails }) {
  const [content, setContent] = useState('');
  const [model, setModel] = useState(conversation.selected_model);
  const [streaming, setStreaming] = useState(false);
  const isGuest = localStorage.getItem('paios_token') === 'guest';

  // Returns a local mock response so guest mode can explore the interface without backend auth.
  function buildGuestResponse(prompt) {
    if (conversation.interaction_mode === 'web_search') {
      return {
        content: `Guest web search preview for: ${prompt}`,
        search_sources_json: [{ title: 'Example Source', url: 'https://example.com', snippet: 'Guest mode shows how sources will appear above an answer.' }],
      };
    }
    if (conversation.interaction_mode === 'tools') {
      return {
        content: `Guest tool preview for: ${prompt}`,
        tool_calls_json: { name: 'get_current_time', arguments: {}, output: new Date().toISOString() },
      };
    }
    return { content: `Guest chat preview for: ${prompt}` };
  }

  // Sends the prompt and applies server-sent events to the visible message list.
  async function sendMessage() {
    if (!content.trim() || streaming) return;
    const prompt = content;
    const userMessage = { id: crypto.randomUUID(), role: 'user', content: prompt, mode_used: conversation.interaction_mode };
    const assistantMessage = { id: crypto.randomUUID(), role: 'assistant', content: '', mode_used: conversation.interaction_mode };
    setMessages([...messages, userMessage, assistantMessage]);
    setContent('');

    if (isGuest) {
      const guestResponse = buildGuestResponse(prompt);
      setMessages((current) => current.map((message) => message.id === assistantMessage.id ? { ...message, ...guestResponse } : message));
      setRunDetails({ request_id: 'guest', mode: conversation.interaction_mode, model, note: 'Guest mode does not call the backend.' });
      return;
    }

    setStreaming(true);
    let streamed = '';
    try {
      await streamMessage(conversation.id, { content: prompt, model, mode: conversation.interaction_mode }, (event, data) => {
        if (event === 'token') {
          streamed += data.token;
          setMessages((current) => current.map((message) => message.id === assistantMessage.id ? { ...message, content: streamed } : message));
        }
        if (event === 'sources') {
          setMessages((current) => current.map((message) => message.id === assistantMessage.id ? { ...message, search_sources_json: data.sources } : message));
        }
        if (event === 'tool_call') {
          setMessages((current) => current.map((message) => message.id === assistantMessage.id ? { ...message, tool_calls_json: data.tool_call } : message));
        }
        if (event === 'error') {
          setMessages((current) => current.map((message) => message.id === assistantMessage.id ? { ...message, content: data.message } : message));
          setRunDetails(data);
        }
        if (event === 'done') {
          setRunDetails(data);
        }
      });
    } catch (error) {
      const message = error.response?.data?.detail || 'The stream failed before the server could return details.';
      setMessages((current) => current.map((item) => item.id === assistantMessage.id ? { ...item, content: message } : item));
      setRunDetails({ status: 'error', message });
    } finally {
      setStreaming(false);
    }
  }

  // Keyboard handling supports Enter to send and Shift+Enter for new lines.
  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="border-t border-slate-800 p-4">
      <div className="flex gap-3 rounded-2xl bg-slate-900 p-3">
        <textarea value={content} onChange={(event) => setContent(event.target.value)} onKeyDown={handleKeyDown} className="min-h-16 flex-1 resize-none bg-transparent text-white outline-none" placeholder="Message PAIOS..." />
        <div className="flex flex-col gap-2">
          <ModelSelector value={model} onChange={setModel} />
          <button onClick={sendMessage} className="rounded-lg bg-blue-600 px-4 py-2 text-white">Send</button>
        </div>
      </div>
    </div>
  );
}

export default Composer;
