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

// Directly queries the AI Stock Market Analyzer agent.
export function runConversation(query) {
  return api.get(`/v1/?query=${encodeURIComponent(query)}`).then((response) => response.data);
}

// Fetches AI performance history tracking snapshots for a stock.
export function fetchPerformanceHistory(ticker) {
  return api.get(`/v1/snapshots/${encodeURIComponent(ticker)}/performance`).then((response) => response.data);
}


