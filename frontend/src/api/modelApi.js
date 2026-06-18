import api from './axios.js';

// Lists active models from the backend registry.
export function listModels() {
  return api.get('/models').then((response) => response.data);
}
