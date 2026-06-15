import { Bot, User } from "lucide-react";

import { MarkdownRenderer } from "./MarkdownRenderer.jsx";

export function MessageBubble({ message, streaming = false }) {
  const isUser = message.role === "user";
  return (
    <article className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser ? (
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-emerald-700 text-white">
          <Bot size={16} />
        </div>
      ) : null}
      <div
        className={`max-w-[78%] rounded-lg border px-4 py-3 shadow-panel ${
          isUser
            ? "border-emerald-200 bg-emerald-50 text-stone-950"
            : "border-stone-200 bg-white text-stone-900"
        }`}
      >
        <MarkdownRenderer content={message.content} />
        {streaming ? <span className="ml-1 inline-block h-4 w-1 animate-pulse bg-emerald-700" /> : null}
      </div>
      {isUser ? (
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-stone-800 text-white">
          <User size={16} />
        </div>
      ) : null}
    </article>
  );
}

