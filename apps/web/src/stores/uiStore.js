import { create } from "zustand";

export const useUiStore = create((set) => ({
  sidebarOpen: true,
  detailsOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  toggleDetails: () => set((state) => ({ detailsOpen: !state.detailsOpen }))
}));

