from app.face_recognition import recognize_face
from app.iot_simulation import simulate_iot_data
from app.vehicle_security_kernel import run_vehicle_security_reasoning
import asyncio

def orchestrate_security(face_id, door_status, motion_status):
    """Orchestrate face recognition, IoT data, and Semantic Kernel reasoning."""
    # Step 1: Face recognition
    is_authorized, face_message = recognize_face(face_id)

    # Step 2: Simulate IoT data
    iot_data = simulate_iot_data(door_status, motion_status)

    # Step 3: Semantic Kernel reasoning
    reasoning_prompt = f"""
    The vehicle is experiencing the following conditions:
    - Face recognition result: {{face_recognition_result}}.
    - Door sensor status: {{door_sensor_status}}.
    - Motion sensor status: {{motion_sensor_status}}.
    Provide recommendations to secure the vehicle.
    """
    semantic_response = asyncio.run(run_vehicle_security_reasoning(
        reasoning_prompt=reasoning_prompt,
        face_recognition_result=face_message,
        iot_data=iot_data
    ))

    return {
        "faceRecognition": face_message,
        "iotData": iot_data,
        "semanticResponse": semantic_response
    }