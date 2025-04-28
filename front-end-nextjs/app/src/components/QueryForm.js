import { useState } from "react";

const QueryForm = ({ onSubmit }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() === "") {
      alert("Please enter a query.");
      return;
    }
    onSubmit(query);
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: "20px 0" }}>
      <label htmlFor="query" style={{ display: "block", marginBottom: "10px" }}>
        Enter your weather-related query:
      </label>
      <input
        type="text"
        id="query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., How is the weather in Melbourne 3977?"
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <button type="submit" style={{ padding: "10px 20px", cursor: "pointer" }}>
        Submit
      </button>
    </form>
  );
};

export default QueryForm;