'use client';

import { useState } from 'react';
import axios from 'axios';

export default function SemanticKernelVehicleSecurityPage() {
  const [faceId, setFaceId] = useState('');
  const [doorStatus, setDoorStatus] = useState('');
  const [motionStatus, setMotionStatus] = useState('');
  const [fingerprintStatus, setFingerprintStatus] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    setResults(null);
    setError('');

    try {
      const formData = new FormData();
      if (faceId) formData.append('faceId', faceId);
      if (doorStatus) formData.append('doorStatus', doorStatus);
      if (motionStatus) formData.append('motionStatus', motionStatus);
      if (fingerprintStatus) formData.append('fingerprintStatus', fingerprintStatus);

      const response = await axios.post('/api/vehicle-security', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err: any) {
      console.error('Error fetching results:', err);
      setError(err.response?.data?.error || 'An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

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
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '20px auto' }}>
        <label htmlFor="faceId" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Select Face ID (Optional):
        </label>
        <select
          id="faceId"
          value={faceId}
          onChange={(e) => setFaceId(e.target.value)}
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
          }}
        >
          <option value="">-- Select Face ID --</option>
          <option value="owner_face_id_1">Owner Face ID 1</option>
          <option value="owner_face_id_2">Owner Face ID 2</option>
          <option value="unknown_face_id">Unknown Face ID</option>
        </select>

        <label htmlFor="doorStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Door Sensor Status (Optional):
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
          <option value="">-- Select Door Status --</option>
          <option value="closed">Closed</option>
          <option value="forced_open">Forced Open</option>
        </select>

        <label htmlFor="motionStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Motion Sensor Status (Optional):
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
          <option value="">-- Select Motion Status --</option>
          <option value="inactive">Inactive</option>
          <option value="active">Active</option>
        </select>

        <label htmlFor="fingerprintStatus" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
          Fingerprint Status (Optional):
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
          <option value="">-- Select Fingerprint Status --</option>
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
          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px' }}>Analysis</h2>
          <p><strong>Face Recognition:</strong> {results.faceRecognition}</p>
          <p><strong>Threat Level:</strong> <span style={{ color: getThreatLevelColor(results.threatLevel) }}>{results.threatLevel}</span></p>

          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px', marginTop: '20px' }}>IoT Data</h2>
          <p><strong>Door Sensor:</strong> {results.iotData?.door_sensor}</p>
          <p><strong>Motion Sensor:</strong> {results.iotData?.motion_sensor}</p>
          <p><strong>Fingerprint Status:</strong> {results.iotData?.fingerprint_status}</p>

          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px', marginTop: '20px' }}>Actions</h2>
          <ul>
            {results.semanticResponse?.actions?.map((action: string, index: number) => (
              <li key={index}>{action}</li>
            ))}
          </ul>

          <h2 style={{ color: '#333', borderBottom: '2px solid #007BFF', paddingBottom: '10px', marginTop: '20px' }}>Executed Actions</h2>
          <ul>
            {results.actionsExecuted?.map((action: any, index: number) => (
              <li key={index}>{action.message}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}