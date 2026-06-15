import { apiRequest } from "./http.js";

export const messagesApi = {
  list: (conversationId) => apiRequest(`/conversations/${conversationId}/messages`)
};

