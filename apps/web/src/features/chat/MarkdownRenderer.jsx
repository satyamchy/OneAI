import { Copy } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { getCodeText } from "../../lib/markdown.js";

function CodeBlock({ inline, className, children, ...props }) {
  const code = getCodeText(children);
  if (inline) {
    return (
      <code className={className} {...props}>
        {children}
      </code>
    );
  }

  return (
    <div className="relative">
      <button
        className="absolute right-2 top-2 rounded bg-white/10 px-2 py-1 text-xs text-stone-100 hover:bg-white/20"
        onClick={() => navigator.clipboard?.writeText(code)}
        title="Copy code"
      >
        <Copy size={13} />
      </button>
      <code className={className} {...props}>
        {children}
      </code>
    </div>
  );
}

export function MarkdownRenderer({ content }) {
  return (
    <div className="markdown-body text-sm">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: CodeBlock
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

