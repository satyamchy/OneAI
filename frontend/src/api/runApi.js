import api from './axios.js';

// Fetches full model run metadata for the Run Details panel.
export function getModelRun(runId) {
  return api.get(`/model-runs/${runId}`).then((response) => response.data);
}
