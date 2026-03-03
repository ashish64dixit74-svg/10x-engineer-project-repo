import { apiRequest } from "./client";

export function getCollections() {
  return apiRequest("/collections");
}

export function getCollection(id) {
  return apiRequest(`/collections/${id}`);
}

export function createCollection(data) {
  return apiRequest("/collections", { method: "POST", body: data });
}

export function deleteCollection(id) {
  return apiRequest(`/collections/${id}`, { method: "DELETE" });
}
