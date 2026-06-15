import { useMutation, useQuery } from "@tanstack/react-query";

import { analyticsApi } from "../../api/analyticsApi.js";
import { conversationsApi } from "../../api/conversationsApi.js";
import { messagesApi } from "../../api/messagesApi.js";
import { modelsApi } from "../../api/modelsApi.js";
import { queryClient } from "../../app/queryClient.js";

export function useConversationsQuery() {
  return useQuery({
    queryKey: ["conversations"],
    queryFn: conversationsApi.list
  });
}

export function useCreateConversationMutation() {
  return useMutation({
    mutationFn: conversationsApi.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["conversations"] })
  });
}

export function useUpdateConversationMutation() {
  return useMutation({
    mutationFn: ({ id, payload }) => conversationsApi.update(id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["conversations"] })
  });
}

export function useDeleteConversationMutation() {
  return useMutation({
    mutationFn: conversationsApi.remove,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["conversations"] })
  });
}

export function useMessagesQuery(conversationId) {
  return useQuery({
    queryKey: ["messages", conversationId],
    queryFn: () => messagesApi.list(conversationId),
    enabled: Boolean(conversationId)
  });
}

export function useModelsQuery() {
  return useQuery({
    queryKey: ["models"],
    queryFn: modelsApi.list
  });
}

export function useUsageQuery() {
  return useQuery({
    queryKey: ["usage"],
    queryFn: analyticsApi.usage
  });
}

