import Button from "../shared/Button";

function formatDate(isoDate) {
  if (!isoDate) {
    return "-";
  }
  return new Date(isoDate).toLocaleString();
}

function PromptDetail({ prompt, collectionName, onBack, onEdit, onDelete }) {
  return (
    <article className="prompt-detail">
      <h1>{prompt.title}</h1>
      <p>{prompt.description || "No description"}</p>

      <section>
        <h2>Content</h2>
        <pre className="prompt-content">{prompt.content}</pre>
      </section>

      <section>
        <h2>Meta</h2>
        <p>Collection: {collectionName || "Unassigned"}</p>
        <p>Created: {formatDate(prompt.created_at)}</p>
        <p>Updated: {formatDate(prompt.updated_at)}</p>
      </section>

      <section>
        <h2>Tags</h2>
        <div className="tag-list">
          {(prompt.tags || []).length
            ? prompt.tags.map((tag) => (
                <span key={tag} className="tag-chip">
                  {tag}
                </span>
              ))
            : "No tags"}
        </div>
      </section>

      <div className="action-row">
        <Button variant="secondary" onClick={onBack}>
          Back
        </Button>
        <Button onClick={onEdit}>Edit</Button>
        <Button variant="danger" onClick={onDelete}>
          Delete
        </Button>
      </div>
    </article>
  );
}

export default PromptDetail;
