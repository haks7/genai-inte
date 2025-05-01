'use client';

import { useState } from 'react';
import axios from 'axios';

export default function TestPage() {
  const [selectedQuery, setSelectedQuery] = useState('');
  const [customQuery, setCustomQuery] = useState(''); // State for custom query
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [selectedCity, setSelectedCity] = useState('Melbourne'); // Default city
  const [postalCode, setPostalCode] = useState('3000'); // Default postal code
  const [previewQuery, setPreviewQuery] = useState(''); // State for query preview
  const [error, setError] = useState(''); // State for error messages

  // Predefined list of Australian cities and postal codes
  const australianCities = [
    { city: 'Melbourne', postalCode: '3000' },
    { city: 'Sydney', postalCode: '2000' },
    { city: 'Brisbane', postalCode: '4000' },
    { city: 'Adelaide', postalCode: '5000' },
    { city: 'Perth', postalCode: '6000' },
    { city: 'Hobart', postalCode: '7000' },
    { city: 'Darwin', postalCode: '0800' },
    { city: 'Canberra', postalCode: '2600' },
  ];

  const handleCityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = australianCities.find((city) => city.city === e.target.value);
    if (selected) {
      setSelectedCity(selected.city);
      setPostalCode(selected.postalCode);
    }
  };

  const handlePreview = () => {
    const queryToPreview = customQuery || selectedQuery || `What is the weather like in ${selectedCity}, ${postalCode}?`;
    setPreviewQuery(queryToPreview);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate inputs
    if (!selectedCity || !postalCode) {
      alert('Please select a valid city and postal code.');
      return;
    }

    const queryToSubmit = customQuery || selectedQuery || `What is the weather like in ${selectedCity}, ${postalCode}?`;

    setLoading(true);
    setResults(null);
    setError('');

    try {
      const response = await axios.post('/api/vehicle-optimization', {
        query: queryToSubmit,
        city: selectedCity, // Send city as a separate field
        postalCode, // Send postal code as a separate field
      });

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
      <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '20px' }}>Weather Query App</h1>
      <p style={{ textAlign: 'center', color: '#555', marginBottom: '20px' }}>
        Select a city and postal code to get weather insights and recommendations.
      </p>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '20px auto' }}>
        <label htmlFor="city" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Select City:
        </label>
        <select
          id="city"
          value={selectedCity}
          onChange={handleCityChange}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          {australianCities.map((city, index) => (
            <option key={index} value={city.city}>
              {city.city} ({city.postalCode})
            </option>
          ))}
        </select>

        <label htmlFor="postalCode" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Postal Code (auto-filled):
        </label>
        <input
          id="postalCode"
          type="text"
          value={postalCode}
          readOnly
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
            backgroundColor: '#f9f9f9',
            color: '#555',
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
            <strong>Car Seat Adjustment:</strong>
            <p>{results.carSeatAdjustment || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>City Weather:</strong>
            <p>
              City: {results.cityWeather?.city || 'N/A'}, Temperature: {results.cityWeather?.temperature || 'N/A'}°C, Condition:{' '}
              {results.cityWeather?.condition || 'N/A'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}