import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import Button from "../components/shared/Button";
import CollectionList from "../components/collections/CollectionList";

function Sidebar({
  collections,
  collectionsLoading,
  selectedCollection,
  onSelectCollection,
  onOpenCollectionModal,
}) {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

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
          <CollectionList
            collections={collections}
            selectedCollection={selectedCollection}
            onSelectCollection={onSelectCollection}
          />
        )}
      </section>
      </div>
    </aside>
  );
}

export default Sidebar;
