import { useMemo, useState } from "react";
import Button from "../shared/Button";

function toTagsArray(tagsText) {
  if (!tagsText.trim()) {
    return [];
  }

  return [...new Set(tagsText.split(",").map((tag) => tag.trim()).filter(Boolean))];
}

function PromptForm({
  collections,
  onSubmit,
  onCancel,
  initialValues,
  submitLabel = "Save Prompt",
}) {
  const [title, setTitle] = useState(initialValues?.title || "");
  const [content, setContent] = useState(initialValues?.content || "");
  const [description, setDescription] = useState(initialValues?.description || "");
  const [collectionId, setCollectionId] = useState(initialValues?.collection_id || "");
  const [tags, setTags] = useState((initialValues?.tags || []).join(", "));
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const validationError = useMemo(() => {
    if (!title.trim()) {
      return "Title is required.";
    }
    if (content.trim().length < 10) {
      return "Content must be at least 10 characters.";
    }
    return "";
  }, [title, content]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (validationError) {
      setError(validationError);
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      await onSubmit({
        title: title.trim(),
        content: content.trim(),
        description: description.trim() || null,
        collection_id: collectionId || null,
        tags: toTagsArray(tags),
      });
    } catch (err) {
      setError(err.message || "Failed to save prompt.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <label>
        Title
        <input value={title} onChange={(event) => setTitle(event.target.value)} required />
      </label>

      <label>
        Content
        <textarea
          value={content}
          onChange={(event) => setContent(event.target.value)}
          rows={8}
          required
        />
      </label>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          rows={3}
        />
      </label>

      <label>
        Collection
        <select
          value={collectionId}
          onChange={(event) => setCollectionId(event.target.value)}
        >
          <option value="">None</option>
          {collections.map((collection) => (
            <option key={collection.id} value={collection.id}>
              {collection.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Tags (comma-separated)
        <input value={tags} onChange={(event) => setTags(event.target.value)} />
      </label>

      {error ? <p className="form-error">{error}</p> : null}

      <div className="action-row">
        <Button type="submit" disabled={submitting}>
          {submitting ? "Saving..." : submitLabel}
        </Button>
        <Button variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  );
}

export default PromptForm;
