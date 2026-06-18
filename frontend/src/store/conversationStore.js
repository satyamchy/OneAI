import { create } from 'zustand';

// Stores conversations and the active conversation selection.
export const useConversationStore = create((set) => ({
  conversations: [],
  activeConversation: null,
  setConversations: (conversations) => set({ conversations }),
  setActiveConversation: (activeConversation) => set({ activeConversation }),
  upsertConversation: (conversation) => set((state) => ({
    conversations: [conversation, ...state.conversations.filter((item) => item.id !== conversation.id)],
    activeConversation: state.activeConversation?.id === conversation.id ? conversation : state.activeConversation,
  })),
}));
