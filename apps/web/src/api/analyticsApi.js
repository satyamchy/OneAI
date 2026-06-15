import { apiRequest } from "./http.js";

export const analyticsApi = {
  usage: () => apiRequest("/analytics/usage")
};

