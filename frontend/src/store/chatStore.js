import { create } from 'zustand';

// Stores messages and streaming status for the active chat.
export const useChatStore = create((set) => ({
  messages: [],
  streaming: false,
  setMessages: (messages) => set({ messages }),
  setStreaming: (streaming) => set({ streaming }),
  appendMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  updateLastAssistant: (content) => set((state) => ({
    messages: state.messages.map((message, index) => (
      index === state.messages.length - 1 ? { ...message, content } : message
    )),
  })),
}));
