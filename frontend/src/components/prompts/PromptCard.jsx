import { useNavigate } from "react-router-dom";

function formatDate(isoDate) {
  if (!isoDate) {
    return "-";
  }
  return new Date(isoDate).toLocaleString();
}

function PromptCard({ prompt }) {
  const navigate = useNavigate();

  return (
    <article
      className="prompt-card"
      tabIndex={0}
      role="button"
      onClick={() => navigate(`/prompts/${prompt.id}`)}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          navigate(`/prompts/${prompt.id}`);
        }
      }}
    >
      <h3>{prompt.title}</h3>
      <p>{prompt.description || prompt.content.slice(0, 120)}</p>
      <div className="tag-list">
        {(prompt.tags || []).map((tag) => (
          <span key={tag} className="tag-chip">
            {tag}
          </span>
        ))}
      </div>
      <small>Updated: {formatDate(prompt.updated_at)}</small>
    </article>
  );
}

export default PromptCard;
