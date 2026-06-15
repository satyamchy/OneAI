import { EmptyState } from "../../components/ui/EmptyState.jsx";
import { MessageBubble } from "./MessageBubble.jsx";

export function MessageList({ messages, streamingContent }) {
  if (!messages.length && !streamingContent) {
    return (
      <EmptyState
        title="Start a conversation"
        description="Send a prompt and the Phase 1 message chain will stream a response."
      />
    );
  }

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-4 px-6 py-6">
      {messages.map((message) => (
        <MessageBubble key={message.id || message.local_id} message={message} />
      ))}
      {streamingContent ? (
        <MessageBubble
          streaming
          message={{
            id: "streaming",
            role: "assistant",
            content: streamingContent
          }}
        />
      ) : null}
    </div>
  );
}

