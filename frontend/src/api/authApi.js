import api from './axios.js';

// Registers a new user account.
export function registerUser(payload) {
  return api.post('/auth/register', payload).then((response) => response.data);
}

// Logs in an existing user account.
export function loginUser(payload) {
  return api.post('/auth/login', payload).then((response) => response.data);
}

// Loads the current user from the stored JWT.
export function getMe() {
  return api.get('/auth/me').then((response) => response.data);
}
