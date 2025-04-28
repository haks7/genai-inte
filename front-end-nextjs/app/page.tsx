'use client';

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      const response = await axios.post('/api/query', { query });
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching results:', error);
      alert('An error occurred while processing your query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f9f9f9', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Weather Query App</h1>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '20px auto' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your weather-related query"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />
        <button
          type="submit"
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#007BFF',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: 'pointer',
          }}
        >
          Submit
        </button>
      </form>
      {loading && <p style={{ textAlign: 'center', color: '#007BFF' }}>Loading...</p>}
      {results && (
        <div style={{ marginTop: '20px', maxWidth: '800px', margin: '20px auto', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px' }}>Results</h2>
          <div style={{ marginBottom: '10px' }}>
            <strong>Sentiment Analysis:</strong>
            <p>
              <strong>Sentiment:</strong>{' '}
              <span style={{ color: results.sentimentAnalysis?.sentiment === 'positive' ? 'green' : results.sentimentAnalysis?.sentiment === 'negative' ? 'red' : '#333' }}>
                {results.sentimentAnalysis?.sentiment || 'N/A'}
              </span>
            </p>
            <p>
              <strong>Confidence Scores:</strong> Positive: {results.sentimentAnalysis?.confidenceScores?.positive ?? 'N/A'}, Neutral: {results.sentimentAnalysis?.confidenceScores?.neutral ?? 'N/A'}, Negative: {results.sentimentAnalysis?.confidenceScores?.negative ?? 'N/A'}
            </p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Sentiment Response:</strong>
            <p>{results.sentimentResponse || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Decisions:</strong>
            <ul>
              {results.decisions?.map((decision: string, index: number) => (
                <li key={index} style={{ marginBottom: '10px' }}>{decision}</li>
              ))}
            </ul>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Car Seat Adjustment:</strong>
            <p>{results.carSeatAdjustment || 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}