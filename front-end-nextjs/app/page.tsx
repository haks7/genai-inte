'use client';

import { useState } from 'react';
import axios from 'axios';

export default function TestPage() {
  const [customQuery, setCustomQuery] = useState(''); // State for custom query
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [selectedCity, setSelectedCity] = useState('Melbourne'); // Default city
  const [postalCode, setPostalCode] = useState('3000'); // Default postal code
  const [selectedCountry, setSelectedCountry] = useState('Australia'); // Default postal code
  const [previewQuery, setPreviewQuery] = useState(''); // State for query preview
  const [error, setError] = useState(''); // State for error messages

  const handlePreview = () => {
    const queryToPreview = customQuery || `Plan my trip efficiently in ${selectedCity}, ${postalCode}.`;
    setPreviewQuery(queryToPreview);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const queryToSubmit = customQuery || `Plan my trip efficiently in ${selectedCity}, ${postalCode}.`;

    setLoading(true);
    setResults(null);
    setError('');

    try {
      const response = await axios.post('/api/vehicle-optimization', {
        query: queryToSubmit,
        city: selectedCity, // Send city as a separate field
        country: selectedCountry,
        postalCode:selectedCountry, // Send postal code as a separate field
      });
      console.log('Response:', response.data); // Log the response data for debugging
      setResults(response.data);
    } catch (error: any) {
      console.error('Error fetching results:', error);
      setError(error.response?.data?.error || 'An error occurred while processing your query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: '20px',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#f9f9f9',
        minHeight: '100vh',
      }}
    >
      <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '20px' }}>Vehicle Optimization App</h1>
      <p style={{ textAlign: 'center', color: '#555', marginBottom: '20px' }}>
        All fields are optional and if no entry is made Melbourne is set to default with a query to know if we have to adjust carseat based on weather API fetced results.
      </p>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '20px auto' }}>
        <label htmlFor="city" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          City (default: Melbourne):
        </label>
        <input
          id="city"
          type="text"
          value={selectedCity}
          onChange={(e) => setSelectedCity(e.target.value)}
          placeholder="Enter city"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />

        <label htmlFor="postalCode" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Postal Code (default: 3000):
        </label>
        <input
          id="postalCode"
          type="text"
          value={postalCode}
          onChange={(e) => setPostalCode(e.target.value)}
          placeholder="Enter postal code"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />

        <label htmlFor="selectedCountry" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Country (default: Australia):
        </label>
        <input
          id="selectedCountry"  
          type="text"
          value={selectedCountry}
          onChange={(e) => setSelectedCountry(e.target.value)}
          placeholder="Enter country"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />

        <label htmlFor="customQuery" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Custom Query (optional):
        </label>
        <input
          id="customQuery"
          type="text"
          value={customQuery}
          onChange={(e) => setCustomQuery(e.target.value)}
          placeholder="E.g., Should I carry an umbrella today?"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />

        <button
          type="button"
          onClick={handlePreview}
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#6c757d',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: 'pointer',
            marginBottom: '20px',
          }}
        >
          Preview Query
        </button>
        {previewQuery && (
          <div
            style={{
              marginBottom: '20px',
              padding: '10px',
              backgroundColor: '#e9ecef',
              borderRadius: '4px',
              fontSize: '16px',
              color: '#333',
            }}
          >
            <strong>Query Preview:</strong> {previewQuery}
          </div>
        )}
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
      {error && (
        <p style={{ textAlign: 'center', color: 'red', marginTop: '20px' }}>
          <strong>Error:</strong> {error}
        </p>
      )}
      {results && (
        <div
          style={{
            marginTop: '20px',
            maxWidth: '800px',
            margin: '20px auto',
            backgroundColor: '#fff',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px' }}>Results</h2>
          <div style={{ marginBottom: '10px' }}>
            <strong>Sentiment Analysis:</strong>
            <p>{results.sentimentAnalysis || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Key Phrases:</strong>
            <p>{results.keyPhrases || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Semantic Response:</strong>
            <p>{results.semanticResponse || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Decision Making:</strong>
            <p>{results.decisionmaking || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Car Seat Heat Adjustment:</strong>
            <p>{results.carSeatHeatAdjustment || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Route Plan:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
              {JSON.stringify(results.routePlan, null, 2) || 'N/A'}
            </pre>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Car Preparation:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
              {JSON.stringify(results.carPreparation, null, 2) || 'N/A'}
            </pre>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Rest Stop Suggestion:</strong>
            <p>{results.restStopSuggestion || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>City Weather:</strong>
            <p>
              City: {results.cityWeather?.city || 'N/A'}, Temperature: {results.cityWeather?.temperature || 'N/A'}°C,
              Condition: {results.cityWeather?.condition || 'N/A'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}