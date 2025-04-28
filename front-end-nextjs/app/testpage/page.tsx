'use client';

import { useState } from 'react';

export default function TestPage() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleTest = () => {
    setLoading(true);

    // Mock backend response
    const mockResponse = {
      carSeatAdjustment: "Heating ON",
      decisions: [
        "Decision by TemperatureAgent: Based on the weather data provided for Melbourne showing a temperature of -5.0°C and sunny conditions, it is evident that there is a discrepancy in the data as it is unlikely to have sunny weather at such a low temperature.\n\nRecommendation:\nGiven the conflicting weather information of sunny conditions with a temperature of -5.0°C, it is recommended to verify the accuracy of the data or consult a reliable weather source for up-to-date and accurate weather details for Melbourne (postcode 3977). In the case of extreme cold temperatures, it is important to dress warmly, stay indoors as much as possible, and take necessary precautions to stay safe and comfortable. Stay informed and seek reliable weather updates for the most current information.",
        "Decision by ConditionAgent: Based on the weather data provided for Melbourne showing a temperature of -5.0°C and sunny conditions, there appears to be a discrepancy in the data as it is unusual to have sunny weather at such a low temperature.\n\nRecommendation:\nGiven the incongruence in the weather information, it is advisable to verify the accuracy of the data or refer to a reliable weather source for updated and correct weather details for Melbourne (postcode 3977). In the case of extreme cold temperatures, ensure to dress warmly, limit outdoor activities, and take necessary precautions to stay safe and comfortable. Stay informed and seek verified weather updates for accurate guidance on handling the weather conditions."
      ],
      sentimentAnalysis: {
        confidenceScores: {
          negative: 0.0,
          neutral: 1.0,
          positive: 0.0
        },
        id: "1",
        sentences: [
          {
            confidenceScores: {
              negative: 0.0,
              neutral: 1.0,
              positive: 0.0
            },
            length: 28,
            offset: 0,
            sentiment: "neutral",
            text: "What is the weather in 3977?"
          }
        ],
        sentiment: "neutral",
        warnings: []
      },
      sentimentResponse: "Here's the weather update for Melbourne."
    };

    // Simulate a delay to mimic loading
    setTimeout(() => {
      setResults(mockResponse);
      setLoading(false);
    }, 1000);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f9f9f9', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Test Weather Query App</h1>
      <button
        onClick={handleTest}
        style={{
          display: 'block',
          margin: '20px auto',
          padding: '12px 20px',
          backgroundColor: '#007BFF',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          fontSize: '16px',
          cursor: 'pointer',
        }}
      >
        Run Test
      </button>
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