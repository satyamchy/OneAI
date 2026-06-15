import { LogOut, MessageSquarePlus, Pencil, Settings, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";

import { Button } from "../../components/ui/Button.jsx";
import { formatDate } from "../../lib/formatDate.js";
import { useAuthStore } from "../../stores/authStore.js";
import {
  useCreateConversationMutation,
  useDeleteConversationMutation,
  useUpdateConversationMutation
} from "./chatHooks.js";

export function ConversationSidebar({
  conversations,
  selectedConversationId,
  onSelectConversation
}) {
  const user = useAuthStore((state) => state.user);
  const clearSession = useAuthStore((state) => state.clearSession);
  const createConversation = useCreateConversationMutation();
  const updateConversation = useUpdateConversationMutation();
  const deleteConversation = useDeleteConversationMutation();

  async function handleCreate() {
    const conversation = await createConversation.mutateAsync({
      title: "New Conversation"
    });
    onSelectConversation(conversation.id);
  }

  async function handleRename(conversation) {
    const title = window.prompt("Rename conversation", conversation.title);
    if (!title || title === conversation.title) return;
    await updateConversation.mutateAsync({
      id: conversation.id,
      payload: { title }
    });
  }

  async function handleDelete(conversation) {
    await deleteConversation.mutateAsync(conversation.id);
    if (conversation.id === selectedConversationId) {
      onSelectConversation("");
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-white/10 p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-lg font-semibold">OneAI</div>
            <div className="text-xs text-stone-400">{user?.email}</div>
          </div>
          <Link to="/settings" title="Settings">
            <Button className="h-8 w-8 px-0" variant="ghost">
              <Settings size={16} />
            </Button>
          </Link>
        </div>
        <Button className="mt-4 w-full" onClick={handleCreate} disabled={createConversation.isPending}>
          <MessageSquarePlus size={16} />
          New chat
        </Button>
      </div>

      <div className="scrollbar-thin min-h-0 flex-1 overflow-y-auto p-2">
        {conversations.map((conversation) => {
          const active = conversation.id === selectedConversationId;
          return (
            <div
              key={conversation.id}
              className={`group mb-1 rounded-md border px-2 py-2 transition ${
                active
                  ? "border-emerald-500 bg-emerald-900/50"
                  : "border-transparent hover:bg-white/8"
              }`}
            >
              <button
                className="w-full text-left"
                onClick={() => onSelectConversation(conversation.id)}
              >
                <div className="truncate text-sm font-medium">{conversation.title}</div>
                <div className="mt-1 text-xs text-stone-400">
                  {formatDate(conversation.updated_at)}
                </div>
              </button>
              <div className="mt-2 hidden gap-1 group-hover:flex">
                <button
                  className="rounded p-1 text-stone-300 hover:bg-white/10"
                  title="Rename"
                  onClick={() => handleRename(conversation)}
                >
                  <Pencil size={14} />
                </button>
                <button
                  className="rounded p-1 text-stone-300 hover:bg-white/10"
                  title="Delete"
                  onClick={() => handleDelete(conversation)}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      <div className="border-t border-white/10 p-3">
        <Button className="w-full" variant="ghost" onClick={clearSession}>
          <LogOut size={16} />
          Sign out
        </Button>
      </div>
    </div>
  );
}

