import { useMutation, useQuery } from "@tanstack/react-query";

import { authApi } from "../../api/authApi.js";

export function useLoginMutation() {
  return useMutation({ mutationFn: authApi.login });
}

export function useRegisterMutation() {
  return useMutation({ mutationFn: authApi.register });
}

export function useMeQuery(enabled) {
  return useQuery({
    queryKey: ["me"],
    queryFn: authApi.me,
    enabled
  });
}

