import { apiRequest } from "./http.js";

export const conversationsApi = {
  list: () => apiRequest("/conversations"),
  create: (payload = {}) => apiRequest("/conversations", { method: "POST", body: payload }),
  get: (id) => apiRequest(`/conversations/${id}`),
  update: (id, payload) => apiRequest(`/conversations/${id}`, { method: "PATCH", body: payload }),
  remove: (id) => apiRequest(`/conversations/${id}`, { method: "DELETE" })
};

