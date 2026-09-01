import { useState } from 'react';
import { runConversation } from '../../api/conversationApi.js';
import ModelSelector from './ModelSelector.jsx';

function Composer({ conversation, messages, setMessages, setRunDetails }) {
  const [content, setContent] = useState('');
  const [model, setModel] = useState(conversation?.selected_model || 'openai/gpt-4o-mini');
  const [streaming, setStreaming] = useState(false);

  // Sends prompt to AI Stock Market Analyzer backend API endpoint
  async function sendMessage() {
    if (!content.trim() || streaming) return;
    const prompt = content;
    const userMessage = { id: crypto.randomUUID(), role: 'user', content: prompt };
    const assistantMessage = { id: crypto.randomUUID(), role: 'assistant', content: 'Analyzing market data & indicators...' };
    setMessages([...messages, userMessage, assistantMessage]);
    setContent('');
    setStreaming(true);

    try {
      const response = await runConversation(prompt);
      setMessages((current) => current.map((message) => 
        message.id === assistantMessage.id ? {
          ...message,
          content: response.answer,
          search_sources_json: response.sources,
          structured_data: response.structured_data,
        } : message
      ));
      if (setRunDetails) {
        setRunDetails({ status: 'success', query: prompt });
      }
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to analyze stock query.';
      setMessages((current) => current.map((message) => 
        message.id === assistantMessage.id ? { ...message, content: `❌ Error: ${errorMsg}` } : message
      ));
      if (setRunDetails) {
        setRunDetails({ status: 'error', message: errorMsg });
      }
    } finally {
      setStreaming(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="border-t border-slate-800 p-4">
      <div className="flex gap-3 rounded-2xl bg-slate-900 p-3">
        <textarea 
          value={content} 
          onChange={(event) => setContent(event.target.value)} 
          onKeyDown={handleKeyDown} 
          className="min-h-16 flex-1 resize-none bg-transparent text-white outline-none placeholder:text-slate-500" 
          placeholder="Ask AI Analyst e.g. 'Analyze TCS for intraday', 'Show market overview', 'Find stocks with strong momentum'..." 
        />
        <div className="flex flex-col gap-2">
          <ModelSelector value={model} onChange={setModel} />
          <button 
            onClick={sendMessage} 
            disabled={streaming}
            className="rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50"
          >
            {streaming ? 'Analyzing...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Composer;
