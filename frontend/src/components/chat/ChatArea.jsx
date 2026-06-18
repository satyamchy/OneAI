import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble.jsx';

function ChatArea({ messages }) {
  const bottomRef = useRef(null);

  // Auto-scroll keeps streamed tokens visible as they arrive.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 space-y-4 overflow-y-auto p-6">
      {messages.map((message) => <MessageBubble key={message.id} message={message} />)}
      <div ref={bottomRef} />
    </div>
  );
}

export default ChatArea;
