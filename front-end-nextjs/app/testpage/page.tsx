'use client';

import { useState } from 'react';

export default function TestPage() {
  const mockResults = {
    sentimentAnalysis:
      "The sentiment analysis of the query indicates: {'sentiment': 'neutral', 'confidenceScores': {'positive': 0.0, 'neutral': 1.0, 'negative': 0.0}, 'statement': \"The sentiment is neutral with a confidence score of 1.00. Seems like you're feeling okay.\"}.",
    keyPhrases: 'The key phrases extracted from the query are: car seat heat adjustment.',
    decisionmaking:
      "The decision based on the query and key phrases is: With Melbourne's temperature at **22.95°C** and **overcast clouds**, **car seat heat adjustment is not strictly needed**. The weather is mild and generally comfortable for driving without additional heat.\n\n### Key Considerations:\n1. **Time of Day**: If driving early morning or late evening when cooler temperatures can be felt, car seat heat adjustment may improve comfort.  \n2. **Personal Sensitivity**: If you tend to feel cold, enabling seat heating for brief moments might help.\n\nIn most scenarios under current conditions, **car seat heat adjustment is unnecessary**. Enjoy your drive! 🚗☁️.",
    carSeatHeatAdjustment: 'The car seat heat adjustment recommendation is: No heating adjustment needed based on temperature.',
    routePlan:
      '1. **Start in Melbourne CBD** and head to **The Loving Hut (Richmond)** (~4 km via Flinders Street) for a vegan breakfast in a calm setting.  \n2. Proceed to **Royal Botanic Gardens Melbourne** (~3 km via St Kilda Road) to relax in nature, paired with calming music.  \n3. Drive to **Home Vegan Bar (Melbourne Central)** (~2 km via Batman Avenue) for lunch, offering fresh vegan options.  \n4. Visit **Docklands Waterfront** (~3 km via La Trobe Street) for a peaceful stroll by the harbor with serene views.  \n5. Return to **Melbourne CBD** (~2 km) via the shortest route to conserve battery and close the loop efficiently.  \n\nThis route optimizes distance, conserves energy, and addresses preferences for vegan food and calming experiences. 🚗🌱',
    carPreparation: { climate: 'Set to 22.95°C', music: 'Playing calm' },
    restStopSuggestion: 'Serotonin Eatery, Royal Botanic Gardens Melbourne, State Library of Victoria, Home Vegan Bar, Docklands Waterfront',
    cityWeather: { city: 'Melbourne', temperature: 22.95, condition: 'overcast clouds' },
  };

  const [results] = useState(mockResults);

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
            {results.routePlan || 'N/A'}
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
    </div>
  );
}