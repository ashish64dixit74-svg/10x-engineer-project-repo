import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import Button from "../components/shared/Button";
import CollectionList from "../components/collections/CollectionList";
import Modal from "../components/shared/Modal";
import ErrorMessage from "../components/shared/ErrorMessage";

function Sidebar({
  collections,
  collectionsLoading,
  selectedCollection,
  onSelectCollection,
  onOpenCollectionModal,
  onDeleteCollection,
}) {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const [collectionToDelete, setCollectionToDelete] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState("");

  const handleConfirmDelete = async () => {
    if (!collectionToDelete) {
      return;
    }

    setIsDeleting(true);
    setDeleteError("");
    try {
      await onDeleteCollection(collectionToDelete.id);
      setCollectionToDelete(null);
    } catch (error) {
      setDeleteError(error.message || "Failed to delete collection.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <aside className={`app-sidebar ${isOpen ? "open" : ""}`}>
      <button
        type="button"
        className="sidebar-mobile-toggle"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-controls="sidebar-content"
      >
        {isOpen ? "Close Menu" : "Open Menu"}
      </button>
      <div id="sidebar-content" className="sidebar-content">
      <div className="sidebar-top">
        <Link to="/" className="sidebar-link">
          Dashboard
        </Link>
        <button
          type="button"
          className={selectedCollection === "" ? "collection-item active" : "collection-item"}
          onClick={() => onSelectCollection("")}
          aria-current={location.pathname === "/" && !selectedCollection ? "page" : undefined}
        >
          All Prompts
        </button>
      </div>

      <section className="sidebar-section">
        <div className="sidebar-title-row">
          <h2>Collections</h2>
          <Button variant="secondary" onClick={onOpenCollectionModal}>
            New
          </Button>
        </div>

        {collectionsLoading ? (
          <p>Loading collections...</p>
        ) : (
          <>
            {deleteError ? <ErrorMessage message={deleteError} /> : null}
            <CollectionList
              collections={collections}
              selectedCollection={selectedCollection}
              onSelectCollection={onSelectCollection}
              onRequestDeleteCollection={(collection) => {
                setDeleteError("");
                setCollectionToDelete(collection);
              }}
            />
          </>
        )}
      </section>
      </div>

      <Modal
        isOpen={Boolean(collectionToDelete)}
        title="Delete this collection?"
        onClose={() => {
          if (!isDeleting) {
            setCollectionToDelete(null);
          }
        }}
        footer={(
          <>
            <Button
              variant="secondary"
              onClick={() => setCollectionToDelete(null)}
              disabled={isDeleting}
            >
              Cancel
            </Button>
            <Button variant="danger" onClick={handleConfirmDelete} disabled={isDeleting}>
              {isDeleting ? "Deleting..." : "Delete"}
            </Button>
          </>
        )}
      >
        <p>This action cannot be undone.</p>
      </Modal>
    </aside>
  );
}

export default Sidebar;
