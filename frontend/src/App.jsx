import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./layouts/Layout";
import Sidebar from "./layouts/Sidebar";
import Dashboard from "./pages/Dashboard";
import PromptPage from "./pages/PromptPage";
import Modal from "./components/shared/Modal";
import CollectionForm from "./components/collections/CollectionForm";
import { useCollections } from "./hooks/useCollections";

function App() {
  const [selectedCollection, setSelectedCollection] = useState("");
  const [showCollectionModal, setShowCollectionModal] = useState(false);
  const {
    collections,
    loading: collectionsLoading,
    error: collectionsError,
    addCollection,
    removeCollection,
  } = useCollections();

  const handleCreateCollection = async (payload) => {
    const created = await addCollection(payload);
    setSelectedCollection(created.id);
    return created;
  };

  const handleDeleteCollection = async (collectionId) => {
    await removeCollection(collectionId);
    if (selectedCollection === collectionId) {
      setSelectedCollection("");
    }
  };

  return (
    <BrowserRouter>
      <Layout
        sidebar={
          <Sidebar
            collections={collections}
            collectionsLoading={collectionsLoading}
            selectedCollection={selectedCollection}
            onSelectCollection={setSelectedCollection}
            onOpenCollectionModal={() => setShowCollectionModal(true)}
            onDeleteCollection={handleDeleteCollection}
          />
        }
      >
        <Routes>
          <Route
            path="/"
            element={
              <Dashboard
                collections={collections}
                selectedCollection={selectedCollection}
                onSelectCollection={setSelectedCollection}
                onCreateCollection={handleCreateCollection}
                collectionsError={collectionsError}
              />
            }
          />
          <Route path="/prompts/:id" element={<PromptPage collections={collections} />} />
        </Routes>

        <Modal
          isOpen={showCollectionModal}
          title="Create Collection"
          onClose={() => setShowCollectionModal(false)}
        >
          <CollectionForm
            onSubmit={async (payload) => {
              await handleCreateCollection(payload);
              setShowCollectionModal(false);
            }}
            onCancel={() => setShowCollectionModal(false)}
          />
        </Modal>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
