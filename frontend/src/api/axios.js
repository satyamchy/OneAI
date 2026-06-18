import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/v1',
});

// Adds the stored JWT to every API request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('paios_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Clears invalid sessions and sends the user back to login.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('paios_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);

export default api;
