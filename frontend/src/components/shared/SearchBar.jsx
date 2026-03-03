import { useEffect, useState } from "react";

function SearchBar({ onSearchChange, delay = 350 }) {
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      onSearchChange(inputValue.trim());
    }, delay);

    return () => clearTimeout(timer);
  }, [inputValue, delay, onSearchChange]);

  return (
    <label className="search-wrap">
      <span className="sr-only">Search prompts</span>
      <input
        className="search-input"
        type="search"
        placeholder="Search by title, content, or description"
        value={inputValue}
        onChange={(event) => setInputValue(event.target.value)}
      />
    </label>
  );
}

export default SearchBar;
