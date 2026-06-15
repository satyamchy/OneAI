import { useEffect, useMemo, useState } from "react";

import { queryClient } from "../../app/queryClient.js";
import { EmptyState } from "../../components/ui/EmptyState.jsx";
import { AppLayout } from "../../layouts/AppLayout.jsx";
import { streamChat } from "../../lib/streamChat.js";
import { useChatStore } from "../../stores/chatStore.js";
import { RunDetailsPanel } from "../run-details/RunDetailsPanel.jsx";
import { ChatWindow } from "./ChatWindow.jsx";
import { ConversationSidebar } from "./ConversationSidebar.jsx";
import {
  useConversationsQuery,
  useCreateConversationMutation,
  useMessagesQuery,
  useModelsQuery,
  useUsageQuery
} from "./chatHooks.js";

export function ChatPage() {
  const [liveMessages, setLiveMessages] = useState([]);
  const [streamingContent, setStreamingContent] = useState("");
  const [streamError, setStreamError] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const selectedConversationId = useChatStore((state) => state.selectedConversationId);
  const selectedMessageModelId = useChatStore((state) => state.selectedMessageModelId);
  const lastRun = useChatStore((state) => state.lastRun);
  const setSelectedConversationId = useChatStore((state) => state.setSelectedConversationId);
  const setSelectedMessageModelId = useChatStore((state) => state.setSelectedMessageModelId);
  const setLastRun = useChatStore((state) => state.setLastRun);

  const conversationsQuery = useConversationsQuery();
  const modelsQuery = useModelsQuery();
  const usageQuery = useUsageQuery();
  const createConversation = useCreateConversationMutation();
  const messagesQuery = useMessagesQuery(selectedConversationId);

  const conversations = conversationsQuery.data || [];
  const models = modelsQuery.data || [];
  const messages = useMemo(() => messagesQuery.data || [], [messagesQuery.data]);

  const selectedConversation = conversations.find(
    (conversation) => conversation.id === selectedConversationId
  );

  useEffect(() => {
    if (!selectedConversationId && conversations.length) {
      setSelectedConversationId(conversations[0].id);
    }
  }, [conversations, selectedConversationId, setSelectedConversationId]);

  useEffect(() => {
    setLiveMessages(messages);
  }, [messages]);

  async function ensureConversation() {
    if (selectedConversationId) {
      return selectedConversationId;
    }
    const conversation = await createConversation.mutateAsync({ title: "New Conversation" });
    setSelectedConversationId(conversation.id);
    return conversation.id;
  }

  function appendOrReplaceMessage(message) {
    setLiveMessages((current) => {
      const exists = current.some((item) => item.id === message.id);
      if (exists) {
        return current.map((item) => (item.id === message.id ? message : item));
      }
      return [...current, message];
    });
  }

  async function handleSend(content, overrideModelId = selectedMessageModelId) {
    const conversationId = await ensureConversation();
    setStreamError("");
    setStreamingContent("");
    setIsStreaming(true);

    try {
      await streamChat({
        conversationId,
        payload: {
          content,
          model_id: overrideModelId || null
        },
        onEvent: (event, data) => {
          if (event === "message_start") {
            appendOrReplaceMessage(data.user_message);
            setLastRun(data.run);
          }
          if (event === "token") {
            setStreamingContent((current) => current + data.content);
          }
          if (event === "model_fallback") {
            setLastRun((lastRunValue) => ({
              ...(lastRunValue || {}),
              request_id: data.request_id,
              fallback_used: true,
              fallback_from_model_id: data.from_model_id,
              model_id: data.to_model_id,
              status: "fallback"
            }));
          }
          if (event === "message_done") {
            appendOrReplaceMessage(data.assistant_message);
            setLastRun(data.run);
            setStreamingContent("");
          }
          if (event === "error") {
            setStreamError(data.message || "Model request failed");
          }
        }
      });
    } catch (error) {
      setStreamError(error.message);
    } finally {
      setIsStreaming(false);
      await queryClient.invalidateQueries({ queryKey: ["conversations"] });
      await queryClient.invalidateQueries({ queryKey: ["messages", conversationId] });
      await queryClient.invalidateQueries({ queryKey: ["usage"] });
    }
  }

  function handleRegenerate() {
    const lastUserMessage = [...liveMessages].reverse().find((message) => message.role === "user");
    if (lastUserMessage) {
      handleSend(lastUserMessage.content);
    }
  }

  const main = selectedConversation ? (
    <ChatWindow
      conversation={selectedConversation}
      messages={liveMessages}
      models={models}
      selectedModelId={selectedMessageModelId}
      onModelChange={setSelectedMessageModelId}
      onSend={handleSend}
      onRegenerate={handleRegenerate}
      isLoading={messagesQuery.isLoading}
      isStreaming={isStreaming}
      streamingContent={streamingContent}
      error={streamError}
    />
  ) : (
    <div className="h-full">
      <EmptyState title="No conversation selected" description="Create a chat to begin." />
    </div>
  );

  return (
    <AppLayout
      sidebar={
        <ConversationSidebar
          conversations={conversations}
          selectedConversationId={selectedConversationId}
          onSelectConversation={setSelectedConversationId}
        />
      }
      main={main}
      details={<RunDetailsPanel run={lastRun} usage={usageQuery.data} />}
    />
  );
}

