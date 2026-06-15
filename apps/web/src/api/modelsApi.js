import { apiRequest } from "./http.js";

export const modelsApi = {
  list: () => apiRequest("/models")
};

