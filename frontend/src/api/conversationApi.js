import api from './axios.js';

// Lists all visible conversations for the current user.
export function listConversations() {
  return api.get('/conversations').then((response) => response.data);
}

// Creates a new conversation.
export function createConversation(payload = {}) {
  return api.post('/conversations', payload).then((response) => response.data);
}

// Updates one conversation, including the selected interaction mode.
export function updateConversation(id, payload) {
  return api.patch(`/conversations/${id}`, payload).then((response) => response.data);
}

// Deletes one conversation.
export function deleteConversation(id) {
  return api.delete(`/conversations/${id}`);
}
