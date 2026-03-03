import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PromptList from "../components/prompts/PromptList";
import PromptForm from "../components/prompts/PromptForm";
import CollectionForm from "../components/collections/CollectionForm";
import SearchBar from "../components/shared/SearchBar";
import Button from "../components/shared/Button";
import Modal from "../components/shared/Modal";
import ErrorMessage from "../components/shared/ErrorMessage";
import { usePrompts } from "../hooks/usePrompts";

function Dashboard({
  collections,
  selectedCollection,
  onSelectCollection,
  onCreateCollection,
  collectionsError,
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [showCreatePrompt, setShowCreatePrompt] = useState(false);
  const [showCreateCollection, setShowCreateCollection] = useState(false);
  const navigate = useNavigate();

  const {
    prompts,
    total,
    loading,
    error,
    reload,
    addPrompt,
  } = usePrompts(selectedCollection, searchQuery);

  const handleCreatePrompt = async (payload) => {
    await addPrompt(payload);
    setShowCreatePrompt(false);
  };

  const handleCreateCollection = async (payload) => {
    const created = await onCreateCollection(payload);
    setShowCreateCollection(false);
    onSelectCollection(created.id);
    navigate("/");
  };

  return (
    <section>
      <div className="toolbar">
        <SearchBar onSearchChange={setSearchQuery} />
        <div className="toolbar-actions">
          <Button onClick={() => setShowCreatePrompt(true)}>Create Prompt</Button>
          <Button variant="secondary" onClick={() => setShowCreateCollection(true)}>
            Create Collection
          </Button>
        </div>
      </div>

      {collectionsError ? <ErrorMessage message={collectionsError} /> : null}
      <p className="subtle-text">Showing {total} prompt(s)</p>
      <PromptList prompts={prompts} loading={loading} error={error} onRetry={reload} />

      <Modal
        isOpen={showCreatePrompt}
        title="Create Prompt"
        onClose={() => setShowCreatePrompt(false)}
      >
        <PromptForm
          collections={collections}
          onSubmit={handleCreatePrompt}
          onCancel={() => setShowCreatePrompt(false)}
          submitLabel="Create Prompt"
        />
      </Modal>

      <Modal
        isOpen={showCreateCollection}
        title="Create Collection"
        onClose={() => setShowCreateCollection(false)}
      >
        <CollectionForm
          onSubmit={handleCreateCollection}
          onCancel={() => setShowCreateCollection(false)}
        />
      </Modal>
    </section>
  );
}

export default Dashboard;
