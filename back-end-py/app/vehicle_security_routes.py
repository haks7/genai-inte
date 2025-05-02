from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.orchestration import orchestrate_security

vehicle_security_routes = Blueprint("vehicle_security_routes", __name__)
CORS(vehicle_security_routes)  # Enable CORS for cross-origin request

@vehicle_security_routes.route('/api/vehicle-security', methods=['POST'])
def vehicle_security():
    """Handle vehicle security requests."""
    try:
        print("Received request at /api/vehicle-security")
        
        # Log headers and raw data for debugging
        print(f"Request headers: {request.headers}")
        print(f"Raw request data: {request.data}")

        # Parse JSON data
        data = request.get_json()
        print(f"Parsed request data: {data}")

        if not data:
            return jsonify({"error": "Invalid or empty JSON payload"}), 400

        # Validate inputs
        face_id = data.get("faceId", "").strip()
        door_status = data.get("doorStatus", "").strip()
        motion_status = data.get("motionStatus", "").strip()
        fingerprint_status = data.get("fingerprint_status", "unknown").strip()  # Default to "unknown"

        if not face_id or not door_status or not motion_status:
            return jsonify({"error": "faceId, doorStatus, and motionStatus are required"}), 400

        # Call the orchestration function
        result = orchestrate_security(face_id, door_status, motion_status, fingerprint_status)
        print(f"Response to front end: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error in vehicle_security route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500