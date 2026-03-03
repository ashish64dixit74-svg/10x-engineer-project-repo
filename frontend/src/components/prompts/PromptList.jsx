import PromptCard from "./PromptCard";
import LoadingSpinner from "../shared/LoadingSpinner";
import ErrorMessage from "../shared/ErrorMessage";

function PromptList({ prompts, loading, error, onRetry }) {
  if (loading) {
    return <LoadingSpinner label="Loading prompts..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={onRetry} />;
  }

  if (!prompts.length) {
    return <p className="empty-state">No prompts found. Create your first one.</p>;
  }

  return (
    <section className="prompt-grid" aria-label="Prompts">
      {prompts.map((prompt) => (
        <PromptCard key={prompt.id} prompt={prompt} />
      ))}
    </section>
  );
}

export default PromptList;
