import { apiRequest } from "./client";

export function getPrompts(queryParams = {}) {
  const searchParams = new URLSearchParams();

  Object.entries(queryParams).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.append(key, String(value));
    }
  });

  const query = searchParams.toString();
  const path = query ? `/prompts?${query}` : "/prompts";
  return apiRequest(path);
}

export function getPrompt(id) {
  return apiRequest(`/prompts/${id}`);
}

export function createPrompt(data) {
  return apiRequest("/prompts", { method: "POST", body: data });
}

export function updatePrompt(id, data) {
  return apiRequest(`/prompts/${id}`, { method: "PUT", body: data });
}

export function patchPrompt(id, data) {
  return apiRequest(`/prompts/${id}`, { method: "PATCH", body: data });
}

export function deletePrompt(id) {
  return apiRequest(`/prompts/${id}`, { method: "DELETE" });
}
