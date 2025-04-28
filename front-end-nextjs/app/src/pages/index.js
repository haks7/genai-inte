import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      const response = await axios.post('/api/query', { query });
      if (response.status !== 200) {
        throw new Error('Failed to fetch results');
      }
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching results:', error);
      alert('An error occurred while processing your query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Weather Query App</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your weather-related query"
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Submit
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {results && (
        <div style={{ marginTop: '20px' }}>
          <h2>Results</h2>
          <pre style={{ background: '#f4f4f4', padding: '10px' }}>
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}