import { RefreshCcw } from "lucide-react";

import { Button } from "../../components/ui/Button.jsx";
import { ErrorState } from "../../components/ui/ErrorState.jsx";
import { Spinner } from "../../components/ui/Spinner.jsx";
import { ChatComposer } from "./ChatComposer.jsx";
import { MessageList } from "./MessageList.jsx";

export function ChatWindow({
  conversation,
  messages,
  models,
  selectedModelId,
  onModelChange,
  onSend,
  onRegenerate,
  isLoading,
  isStreaming,
  streamingContent,
  error
}) {
  return (
    <div className="flex h-full min-w-0 flex-col">
      <header className="flex h-16 items-center justify-between border-b border-stone-200 bg-white px-6">
        <div className="min-w-0">
          <h1 className="truncate text-lg font-semibold text-stone-950">
            {conversation?.title || "OneAI"}
          </h1>
          <p className="text-xs text-stone-500">
            {conversation?.default_model_id || "Conversation default model"}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isLoading ? <Spinner /> : null}
          <Button variant="secondary" onClick={onRegenerate} disabled={isStreaming || !messages.length}>
            <RefreshCcw size={15} />
            Regenerate
          </Button>
        </div>
      </header>

      {error ? (
        <div className="px-6 pt-4">
          <ErrorState message={error} />
        </div>
      ) : null}

      <div className="scrollbar-thin min-h-0 flex-1 overflow-y-auto">
        <MessageList messages={messages} streamingContent={streamingContent} />
      </div>

      <ChatComposer
        models={models}
        selectedModelId={selectedModelId}
        onModelChange={onModelChange}
        onSend={onSend}
        disabled={!conversation || isStreaming}
      />
    </div>
  );
}

