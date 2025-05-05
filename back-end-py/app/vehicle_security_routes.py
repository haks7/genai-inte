from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.orchestration import orchestrate_security

vehicle_security_routes = Blueprint("vehicle_security_routes", __name__)
CORS(vehicle_security_routes)  # Enable CORS for cross-origin requests

@vehicle_security_routes.route('/api/vehicle-security', methods=['POST'])
def vehicle_security():
    """Handle vehicle security requests."""
    try:
        print("Received request at /api/vehicle-security")
        
        # Log headers and raw data for debugging
        print(f"Request headers: {request.headers}")
        print(f"Raw request data: {request.data}")

        # Ensure the request is multipart/form-data
        if not request.content_type.startswith("multipart/form-data"):
            return jsonify({"error": "Unsupported Media Type. Expected 'multipart/form-data'."}), 415

         # Parse multipart/form-data
        face_id = request.form.get("faceId", "unknown").strip()  # Default to "unknown"
        door_status = request.form.get("doorStatus", "unknown").strip()  # Default to "unknown"
        motion_status = request.form.get("motionStatus", "unknown").strip()  # Default to "unknown"
        fingerprint_status = request.form.get("fingerprintStatus", "unknown").strip()  # Default to "unknown"

        # Debugging log for parsed form data
        print(f"Parsed form data: faceId={face_id}, doorStatus={door_status}, motionStatus={motion_status}, fingerprintStatus={fingerprint_status}")

        # Validate required inputs
        if not face_id or not door_status or not motion_status:
            return jsonify({"error": "faceId, doorStatus, and motionStatus are required"}), 400

        # Call the orchestration function
        result = orchestrate_security(face_id, door_status, motion_status, fingerprint_status)
        print(f"Response to front end: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error in vehicle_security route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500