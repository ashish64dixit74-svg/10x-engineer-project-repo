import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import PromptDetail from "../components/prompts/PromptDetail";
import PromptForm from "../components/prompts/PromptForm";
import Modal from "../components/shared/Modal";
import Button from "../components/shared/Button";
import LoadingSpinner from "../components/shared/LoadingSpinner";
import ErrorMessage from "../components/shared/ErrorMessage";
import { deletePrompt, getPrompt, updatePrompt } from "../api/prompts";

function PromptPage({ collections }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const loadPrompt = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const data = await getPrompt(id);
      setPrompt(data);
    } catch (err) {
      setError(err.message || "Failed to load prompt.");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    void loadPrompt();
  }, [loadPrompt]);

  const collectionName = useMemo(() => {
    if (!prompt?.collection_id) {
      return "";
    }
    const matched = collections.find((collection) => collection.id === prompt.collection_id);
    return matched?.name || "Unknown collection";
  }, [collections, prompt]);

  const handleUpdatePrompt = async (payload) => {
    await updatePrompt(id, payload);
    setEditing(false);
    await loadPrompt();
  };

  const handleDelete = async () => {
    await deletePrompt(id);
    navigate("/");
  };

  if (loading) {
    return <LoadingSpinner label="Loading prompt..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={loadPrompt} />;
  }

  if (!prompt) {
    return <p className="empty-state">Prompt not found.</p>;
  }

  return (
    <section>
      <PromptDetail
        prompt={prompt}
        collectionName={collectionName}
        onBack={() => navigate("/")}
        onEdit={() => setEditing(true)}
        onDelete={() => setConfirmDelete(true)}
      />

      <Modal isOpen={editing} title="Edit Prompt" onClose={() => setEditing(false)}>
        <PromptForm
          collections={collections}
          initialValues={prompt}
          submitLabel="Update Prompt"
          onSubmit={handleUpdatePrompt}
          onCancel={() => setEditing(false)}
        />
      </Modal>

      <Modal
        isOpen={confirmDelete}
        title="Delete Prompt"
        onClose={() => setConfirmDelete(false)}
        footer={
          <>
            <Button variant="secondary" onClick={() => setConfirmDelete(false)}>
              Cancel
            </Button>
            <Button variant="danger" onClick={handleDelete}>
              Delete
            </Button>
          </>
        }
      >
        <p>This action cannot be undone. Delete this prompt?</p>
      </Modal>
    </section>
  );
}

export default PromptPage;
