function CollectionList({ collections, selectedCollection, onSelectCollection }) {
  if (!collections.length) {
    return <p className="empty-state">No collections yet.</p>;
  }

  return (
    <ul className="collection-list">
      {collections.map((collection) => (
        <li key={collection.id}>
          <button
            type="button"
            className={collection.id === selectedCollection ? "collection-item active" : "collection-item"}
            onClick={() => onSelectCollection(collection.id)}
          >
            <span>{collection.name}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}

export default CollectionList;
