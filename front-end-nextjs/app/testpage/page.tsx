'use client';

import { useState } from 'react';

export default function TestPage() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleTest = () => {
    setLoading(true);

    // Mock backend response
    const mockResponse = {
      carSeatAdjustment: "The car seat adjustment recommendation is: Heating OFF.",
      cityWeather: {
        city: "Melbourne",
        condition: "Sunny",
        temperature: 15.0,
      },
      decisionmaking:
        "The decision based on the query and key phrases is: It seems like you have positive feelings towards the weather in Melbourne with postcode 3000. Melbourne is known for its diverse weather patterns, ranging from sunny days to mild temperatures and occasional rainy spells. It's a city with a vibrant culture, beautiful parks, and various activities to enjoy in different weather conditions. Whether you appreciate the sunny days for outdoor adventures or the cozy ambiance on rainy days, Melbourne has something for everyone to enjoy. Embrace and savor the unique weather experiences that Melbourne offers in postcode 3000!",
      keyPhrases: "The key phrases extracted from the query are: weather, Melbourne.",
      semanticResponse:
        "The semantic reasoning response is: Based on the user query and extracted key phrases, here are some actionable recommendations for optimizing vehicle operations:\n\n1. Use the weather data to plan routes and schedules: Incorporate the weather data provided to anticipate any potential disruptions or hazards on the road. Adjust.",
      sentimentAnalysis: {
        sentiment: "The sentiment is positive with a confidence score of 1"
      },
    };

    // Simulate a delay to mimic loading
    setTimeout(() => {
      setResults(mockResponse);
      setLoading(false);
    }, 1000);
  };

  return (
    <div
      style={{
        padding: "20px",
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f9f9f9",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ textAlign: "center", color: "#333" }}>
        Test Weather Query App
      </h1>
      <button
        onClick={handleTest}
        style={{
          display: "block",
          margin: "20px auto",
          padding: "12px 20px",
          backgroundColor: "#007BFF",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Run Test
      </button>
      {loading && (
        <p style={{ textAlign: "center", color: "#007BFF" }}>Loading...</p>
      )}
      {results && (
        <div
          style={{
            marginTop: "20px",
            maxWidth: "800px",
            margin: "20px auto",
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "8px",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
          }}
        >
          <h2
            style={{
              color: "#333",
              borderBottom: "2px solid #007BFF",
              paddingBottom: "10px",
            }}
          >
            Results
          </h2>
          <div style={{ marginBottom: "10px" }}>
            <p>
              <strong>Sentiment Analysis:</strong>{" "}
              <span
                style={{
                  color:
                    results.sentimentAnalysis?.sentiment === "positive"
                      ? "green"
                      : results.sentimentAnalysis?.sentiment === "negative"
                      ? "red"
                      : "#333",
                }}
              >
                {results.sentimentAnalysis?.sentiment || "N/A"}
              </span>
            </p>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <strong>Key Phrases:</strong>
            <p>{results.keyPhrases || "N/A"}</p>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <strong>Semantic Response:</strong>
            <p>{results.semanticResponse || "N/A"}</p>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <strong>Decision Making:</strong>
            <p>{results.decisionmaking || "N/A"}</p>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <strong>Car Seat Adjustment:</strong>
            <p>{results.carSeatAdjustment || "N/A"}</p>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <strong>City Weather:</strong>
            <p>
              City: {results.cityWeather?.city || "N/A"}, Temperature:{" "}
              {results.cityWeather?.temperature || "N/A"}°C, Condition:{" "}
              {results.cityWeather?.condition || "N/A"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}