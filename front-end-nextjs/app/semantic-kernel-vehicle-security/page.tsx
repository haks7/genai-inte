'use client';

import { useState } from 'react';
import axios from 'axios';

export default function SemanticKernelVehicleSecurityPage() {
  const [scenario, setScenario] = useState(''); // Dropdown for scenario selection
  const [faceId, setFaceId] = useState(''); // Input for face ID
  const [doorStatus, setDoorStatus] = useState('closed'); // Input for door sensor status
  const [motionStatus, setMotionStatus] = useState('inactive'); // Input for motion sensor status
  const [fingerprintStatus, setFingerprintStatus] = useState('unknown'); // Input for fingerprint status
  const [results, setResults] = useState<any>(null); // Results from the API
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(''); // Error state

  // Predefined scenarios
  const scenarios = {
    positive: {
      faceId: 'owner_face_id_1',
      doorStatus: 'closed',
      motionStatus: 'inactive',
      fingerprintStatus: 'authorized',
    },
    negative: {
      faceId: 'unknown_face_id',
      doorStatus: 'forced_open',
      motionStatus: 'active',
      fingerprintStatus: 'unauthorized',
    },
  };

  // Handle scenario selection
  const handleScenarioChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedScenario = e.target.value;
    setScenario(selectedScenario);

    if (selectedScenario === 'positive') {
      setFaceId(scenarios.positive.faceId);
      setDoorStatus(scenarios.positive.doorStatus);
      setMotionStatus(scenarios.positive.motionStatus);
      setFingerprintStatus(scenarios.positive.fingerprintStatus);
    } else if (selectedScenario === 'negative') {
      setFaceId(scenarios.negative.faceId);
      setDoorStatus(scenarios.negative.doorStatus);
      setMotionStatus(scenarios.negative.motionStatus);
      setFingerprintStatus(scenarios.negative.fingerprintStatus);
    } else {
      setFaceId('');
      setDoorStatus('closed');
      setMotionStatus('inactive');
      setFingerprintStatus('unknown');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate inputs
    if (!faceId) {
      alert('Please provide a valid Face ID.');
      return;
    }

    setLoading(true);
    setResults(null);
    setError('');

    try {
      // Call the /api/vehicle-security endpoint
      const response = await axios.post('/api/vehicle-security', {
        faceId,
        doorStatus,
        motionStatus,
        fingerprint_status: fingerprintStatus, // Include fingerprint status
      });

      setResults(response.data);
    } catch (err: any) {
      console.error('Error fetching results:', err);
      setError(err.response?.data?.error || 'An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

  // Determine the color based on the threat level
  const getThreatLevelColor = (threatLevel: string) => {
    switch (threatLevel) {
      case 'low':
        return '#28a745'; // Green
      case 'medium':
        return '#ffc107'; // Orange
      case 'high':
        return '#dc3545'; // Red
      default:
        return '#6c757d'; // Gray (unknown)
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
      <h1 style={{ textAlign: 'center', color: '#333', marginBottom: '20px' }}>
        Semantic Kernel Vehicle Security
      </h1>
      <p style={{ textAlign: 'center', color: '#555', marginBottom: '20px' }}>
        Test the vehicle security system powered by Semantic Kernel.
      </p>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '20px auto' }}>
        <label htmlFor="scenario" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Select Scenario:
        </label>
        <select
          id="scenario"
          value={scenario}
          onChange={handleScenarioChange}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          <option value="">-- Select Scenario --</option>
          <option value="positive">Positive Scenario (Authorized Access)</option>
          <option value="negative">Negative Scenario (Unauthorized Access)</option>
        </select>

        <label htmlFor="faceId" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Face ID:
        </label>
        <input
          id="faceId"
          type="text"
          value={faceId}
          onChange={(e) => setFaceId(e.target.value)}
          placeholder="Enter Face ID"
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        />

        <label htmlFor="doorStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Door Sensor Status:
        </label>
        <select
          id="doorStatus"
          value={doorStatus}
          onChange={(e) => setDoorStatus(e.target.value)}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          <option value="closed">Closed</option>
          <option value="forced_open">Forced Open</option>
        </select>

        <label htmlFor="motionStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Motion Sensor Status:
        </label>
        <select
          id="motionStatus"
          value={motionStatus}
          onChange={(e) => setMotionStatus(e.target.value)}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          <option value="inactive">Inactive</option>
          <option value="active">Active</option>
        </select>

        <label htmlFor="fingerprintStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Fingerprint Status:
        </label>
        <select
          id="fingerprintStatus"
          value={fingerprintStatus}
          onChange={(e) => setFingerprintStatus(e.target.value)}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          <option value="unknown">Unknown</option>
          <option value="authorized">Authorized</option>
          <option value="unauthorized">Unauthorized</option>
        </select>

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
            borderLeft: `10px solid ${getThreatLevelColor(results.threatLevel)}`,
          }}
        >
          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px' }}>Results</h2>
          <div style={{ marginBottom: '10px' }}>
            <strong>Face Recognition:</strong>
            <p>{results.faceRecognition || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>IoT Data:</strong>
            <p>Door Sensor: {results.iotData?.door_sensor || 'N/A'}</p>
            <p>Motion Sensor: {results.iotData?.motion_sensor || 'N/A'}</p>
            <p>Fingerprint Status: {results.iotData?.fingerprint_status || 'N/A'}</p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Threat Level:</strong>
            <p style={{ color: getThreatLevelColor(results.threatLevel), fontWeight: 'bold' }}>
              {results.threatLevel || 'N/A'}
            </p>
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Actions Executed:</strong>
            <ul>
              {results.actionsExecuted?.map((action: any, index: number) => (
                <li key={index}>{action.message}</li>
              )) || 'N/A'}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}