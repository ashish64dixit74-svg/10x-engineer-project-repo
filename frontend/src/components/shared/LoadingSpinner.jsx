function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="centered-state" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}

export default LoadingSpinner;
