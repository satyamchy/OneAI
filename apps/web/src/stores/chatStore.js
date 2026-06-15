import { create } from "zustand";

export const useChatStore = create((set) => ({
  selectedConversationId: "",
  selectedMessageModelId: "",
  lastRun: null,
  setSelectedConversationId: (selectedConversationId) => set({ selectedConversationId }),
  setSelectedMessageModelId: (selectedMessageModelId) => set({ selectedMessageModelId }),
  setLastRun: (nextRun) =>
    set((state) => ({
      lastRun: typeof nextRun === "function" ? nextRun(state.lastRun) : nextRun
    }))
}));
