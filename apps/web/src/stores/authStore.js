import { create } from "zustand";

const storedToken = localStorage.getItem("oneai_token");
const storedUser = localStorage.getItem("oneai_user");

export const useAuthStore = create((set) => ({
  token: storedToken || "",
  user: storedUser ? JSON.parse(storedUser) : null,
  setSession: ({ access_token, user }) => {
    localStorage.setItem("oneai_token", access_token);
    localStorage.setItem("oneai_user", JSON.stringify(user));
    set({ token: access_token, user });
  },
  clearSession: () => {
    localStorage.removeItem("oneai_token");
    localStorage.removeItem("oneai_user");
    set({ token: "", user: null });
  }
}));

