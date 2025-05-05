from app.vehicle_security_helper import (
    recognize_face,
    simulate_iot_data,
    send_alert_email,
    trigger_vehicle_alarm,
    lock_vehicle,
    run_security_reasoning
)
import asyncio
import os

def orchestrate_security(face_id, door_status, motion_status, fingerprint_status):
    """
    Orchestrates the vehicle security process by integrating face recognition,
    IoT data simulation, Semantic Kernel reasoning, and action execution.
    """
    try:
        # Step 1: Face Recognition
        print("Step 1: Starting face recognition...")
        is_authorized, face_message = recognize_face(face_id)
        print(f"Face recognition result: {face_message}")

        # Step 2: IoT Data Simulation
        print("Step 2: Simulating IoT data...")
        iot_data = simulate_iot_data(door_status, motion_status, fingerprint_status)
        print(f"IoT data: {iot_data}")

        # Step 3: Semantic Kernel Reasoning
        print("Step 3: Running Semantic Kernel reasoning...")
        reasoning_prompt = (
            "Analyze the following vehicle security conditions:\n"
            f"- Face recognition: {face_message}.\n"
            f"- Door sensor: {iot_data['door_sensor']}.\n"
            f"- Motion sensor: {iot_data['motion_sensor']}.\n"
            f"- Fingerprint status: {iot_data['fingerprint_status']}.\n\n"
            "Classify the threat level as 'low', 'medium', or 'high' based on the conditions, and recommend actions to secure the vehicle.\n"
            "Provide the response in validated JSON format with:\n"
            "1. The threat level ('low', 'medium', or 'high').\n"
            "2. A list of recommended actions."
        )

        semantic_response = asyncio.run(run_security_reasoning(
            reasoning_prompt=reasoning_prompt,
            face_message=face_message,
            iot_data=iot_data,
            fingerprint_status=fingerprint_status
        ))
        print(f"Semantic Kernel response: {semantic_response}")

        # Fallback Logic for Incorrect Responses
        if semantic_response["threat_level"] == "low" and (
            face_message == "Unauthorized access detected" or
            iot_data["door_sensor"] == "forced_open" or
            iot_data["motion_sensor"] == "active" or
            fingerprint_status == "unauthorized"
        ):
            print("Fallback: Adjusting threat level to 'high' due to suspicious activity.")
            semantic_response["threat_level"] = "high"
            semantic_response["actions"] = ["lock_vehicle", "send_email"]

        # Parse the Semantic Kernel Response
        threat_level = semantic_response.get("threat_level", "low")
        actions = semantic_response.get("actions", [])

        # Prepare the Response
        response = {
            "faceRecognition": face_message,
            "iotData": iot_data,
            "semanticResponse": semantic_response,
            "threatLevel": threat_level,
            "actionsExecuted": []
        }

        # Execute Actions Based on the Response
        for action in actions:
            if action == "lock_vehicle":
                response["actionsExecuted"].append(lock_vehicle())
            elif action == "trigger_alarm":
                response["actionsExecuted"].append(trigger_vehicle_alarm())
            elif action == "send_email":
                subject = "ALERT: High-Level Threat Detected"
                body = (
                    f"A high-level threat has been detected.\n\n"
                    f"Details:\n"
                    f"- Face Recognition: {face_message}\n"
                    f"- Door Sensor: {iot_data['door_sensor']}\n"
                    f"- Motion Sensor: {iot_data['motion_sensor']}\n"
                    f"- Fingerprint Status: {fingerprint_status}\n\n"
                    f"Immediate action has been taken to secure the vehicle."
                )
                recipient_email = os.getenv("RECIPIENT_EMAIL", "sumana.pinjarla@gmail.com")
                send_alert_email(subject, body, recipient_email)
                response["actionsExecuted"].append({"action": "email_sent", "message": "Alert email sent."})

        # Handle Cases Where No Actions Are Required
        if not response["actionsExecuted"]:
            response["actionsExecuted"].append({"action": "none", "message": "No immediate action required."})

        return response
    except Exception as e:
        print(f"Error in orchestrate_security: {e}")
        raise RuntimeError(f"Failed to orchestrate security: {e}")