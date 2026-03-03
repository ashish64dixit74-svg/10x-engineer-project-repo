import { useMemo, useState } from "react";
import Button from "../shared/Button";

function CollectionForm({ onSubmit, onCancel }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const nameError = useMemo(() => {
    if (!name.trim()) {
      return "Collection name is required.";
    }
    return "";
  }, [name]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (nameError) {
      setError(nameError);
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      await onSubmit({
        name: name.trim(),
        description: description.trim() || null,
      });
    } catch (err) {
      setError(err.message || "Failed to create collection.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <label>
        Name
        <input value={name} onChange={(event) => setName(event.target.value)} required />
      </label>

      <label>
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          rows={3}
        />
      </label>

      {error ? <p className="form-error">{error}</p> : null}

      <div className="action-row">
        <Button type="submit" disabled={submitting}>
          {submitting ? "Saving..." : "Create Collection"}
        </Button>
        <Button variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  );
}

export default CollectionForm;
