import { useEffect, useState } from "react";
import {
  createCollection,
  deleteCollection,
  getCollections,
} from "../api/collections";

export function useCollections() {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const reload = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getCollections();
      setCollections(data.collections || []);
    } catch (err) {
      setError(err.message || "Failed to load collections.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void reload();
  }, []);

  const addCollection = async (payload) => {
    const created = await createCollection(payload);
    await reload();
    return created;
  };

  const removeCollection = async (id) => {
    await deleteCollection(id);
    await reload();
  };

  return { collections, loading, error, reload, addCollection, removeCollection };
}
