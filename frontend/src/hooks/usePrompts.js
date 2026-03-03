import { useCallback, useEffect, useMemo, useState } from "react";
import {
  createPrompt,
  deletePrompt,
  getPrompts,
  patchPrompt,
  updatePrompt,
} from "../api/prompts";

export function usePrompts(selectedCollection, searchQuery) {
  const [prompts, setPrompts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const queryParams = useMemo(
    () => ({
      collection_id: selectedCollection || undefined,
      search: searchQuery || undefined,
    }),
    [selectedCollection, searchQuery],
  );

  const reload = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getPrompts(queryParams);
      setPrompts(data.prompts || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.message || "Failed to load prompts.");
    } finally {
      setLoading(false);
    }
  }, [queryParams]);

  useEffect(() => {
    void reload();
  }, [reload]);

  const addPrompt = async (payload) => {
    const created = await createPrompt(payload);
    await reload();
    return created;
  };

  const replacePrompt = async (id, payload) => {
    const updated = await updatePrompt(id, payload);
    await reload();
    return updated;
  };

  const partialUpdatePrompt = async (id, payload) => {
    const updated = await patchPrompt(id, payload);
    await reload();
    return updated;
  };

  const removePrompt = async (id) => {
    await deletePrompt(id);
    await reload();
  };

  return {
    prompts,
    total,
    loading,
    error,
    reload,
    addPrompt,
    replacePrompt,
    partialUpdatePrompt,
    removePrompt,
  };
}
