import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import SourcesBlock from './SourcesBlock.jsx';
import ToolCallBlock from './ToolCallBlock.jsx';

function MessageBubble({ message }) {
  const isAssistant = message.role === 'assistant';

  // Assistant messages can render sources or tool output above markdown content.
  return (
    <article className={`rounded-2xl p-4 ${isAssistant ? 'bg-slate-900' : 'ml-auto max-w-3xl bg-blue-600'}`}>
      {message.search_sources_json && <SourcesBlock sources={message.search_sources_json} />}
      {message.tool_calls_json && <ToolCallBlock toolCall={message.tool_calls_json} />}
      <ReactMarkdown components={{
        code({ inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? <SyntaxHighlighter language={match[1]} PreTag="div" {...props}>{String(children).replace(/\n$/, '')}</SyntaxHighlighter> : <code className="rounded bg-slate-800 px-1" {...props}>{children}</code>;
        },
      }}>
        {message.content}
      </ReactMarkdown>
      {isAssistant && <button onClick={() => navigator.clipboard.writeText(message.content)} className="mt-3 text-xs text-slate-400">Copy</button>}
    </article>
  );
}

export default MessageBubble;
