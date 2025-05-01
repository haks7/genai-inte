from flask import Blueprint, request, jsonify
from app.orchestration import orchestrate_security

vehicle_security_routes = Blueprint("vehicle_security_routes", __name__)

@vehicle_security_routes.route('/api/vehicle-security', methods=['POST'])
def vehicle_security():
    """Vehicle security endpoint."""
    try:
        # Parse request data
        data = request.get_json()
        face_id = data.get("faceId", "unknown_face_id")
        door_status = data.get("doorStatus", "closed")
        motion_status = data.get("motionStatus", "inactive")

        # Orchestrate the security process
        result = orchestrate_security(face_id, door_status, motion_status)

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        print(f"Error in vehicle_security route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500