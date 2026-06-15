import { Send } from "lucide-react";
import { useState } from "react";

import { Button } from "../../components/ui/Button.jsx";
import { Textarea } from "../../components/ui/Textarea.jsx";
import { ModelSelector } from "./ModelSelector.jsx";

export function ChatComposer({ models, selectedModelId, onModelChange, onSend, disabled }) {
  const [content, setContent] = useState("");

  function submit() {
    const trimmed = content.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setContent("");
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  }

  return (
    <div className="border-t border-stone-200 bg-[#f7f8f5]/95 px-6 py-4">
      <div className="mx-auto max-w-4xl rounded-lg border border-stone-200 bg-white p-3 shadow-panel">
        <Textarea
          rows={3}
          value={content}
          onChange={(event) => setContent(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask OneAI..."
          disabled={disabled}
        />
        <div className="mt-3 flex items-center justify-between gap-3">
          <ModelSelector
            compact
            models={models}
            value={selectedModelId}
            onChange={onModelChange}
          />
          <Button onClick={submit} disabled={disabled || !content.trim()}>
            <Send size={16} />
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}

