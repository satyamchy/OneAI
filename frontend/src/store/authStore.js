import { create } from 'zustand';

// Stores authenticated user data shared across the frontend.
export const useAuthStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));
