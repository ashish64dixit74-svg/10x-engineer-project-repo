function CollectionList({
  collections,
  selectedCollection,
  onSelectCollection,
  onRequestDeleteCollection,
}) {
  if (!collections.length) {
    return <p className="empty-state">No collections yet.</p>;
  }

  return (
    <ul className="collection-list">
      {collections.map((collection) => (
        <li key={collection.id} className="collection-row">
          <button
            type="button"
            className={collection.id === selectedCollection ? "collection-item active" : "collection-item"}
            onClick={() => onSelectCollection(collection.id)}
          >
            <span>{collection.name}</span>
          </button>
          <button
            type="button"
            className="collection-delete-btn"
            aria-label="Delete collection"
            onClick={(event) => {
              event.stopPropagation();
              onRequestDeleteCollection(collection);
            }}
          >
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M9 3.75h6m-8.25 3h10.5m-9.75 0 .75 12h6l.75-12m-5.25 3v6m3-6v6"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </li>
      ))}
    </ul>
  );
}

export default CollectionList;
