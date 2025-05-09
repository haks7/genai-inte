from flask import json
from app.vehicle_security_helper import (
    recognize_face,
    simulate_iot_data,
    send_alert_email,
    trigger_vehicle_alarm,
    lock_vehicle,
)
# DO NOT DELETE THIS LINE
# from app.generate_architecture_diagram import generate_architecture_diagram
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
            "Provide the response in validated JSON format only with:\n"
            "1. The threat level ('low', 'medium', or 'high').\n"
            "2. A list of recommended actions."
        )

        # semantic_response_raw = asyncio.run(run_security_reasoning(
        #     reasoning_prompt=reasoning_prompt,
        #     face_message=face_message,
        #     iot_data=iot_data,
        #     fingerprint_status=fingerprint_status
        # ))

        semantic_response = {
        "threat_level": "high",
        "recommended_actions": [
            "Activate the motion sensor to detect any unauthorized movement around the vehicle.",
            "Investigate the unauthorized fingerprint status and update the access permissions.",
            "Consider implementing additional security measures such as a PIN code or key fob access in addition to face recognition.",
            "Regularly check and maintain the door sensor to ensure it is functioning properly."
        ]
        }        # Run the Semantic Kernel reasoning asynchronously
        # print threat level and actions from the response
        # print(f"Threat level: {semantic_response['threat_level']}")

                # Extract Threat Level and Actions
        try:
            # semantic_response_raw = str(semantic_response_raw)
            # semantic_response = json.loads(semantic_response_raw)
            print(f"Parsed Semantic Kernel response: {semantic_response}")  # Debugging log

            threat_level = semantic_response['threat_level']
            threat_level = threat_level.lower()  # Normalize to lowercase
        except Exception as e:
            print(f"Error reading threat level: {e}")
            threat_level = "unknown"

        print(f"Threat level: {threat_level}")

        # Determine actions based on threat level or fallback logic
        actions_executed = []

        if threat_level == "high":
            print("Executing all actions for high threat level.")
            actions_executed.append(lock_vehicle())
            actions_executed.append(trigger_vehicle_alarm())
            actions_executed.append(send_alert_email())
        elif threat_level == "medium":
            print("Executing lock vehicle and send email for medium threat level.")
            actions_executed.append(lock_vehicle())
            actions_executed.append(send_alert_email())
        elif threat_level == "low":
            print("Executing send email for low threat level.")
            actions_executed.append(send_alert_email())
        else:
            print("Threat level unknown or exception occurred. Applying fallback logic.")
            if (
                face_message == "Unauthorized access detected" and
                iot_data["door_sensor"] == "forced_open" and
                iot_data["motion_sensor"] == "active" and
                fingerprint_status == "unauthorized"
            ):
                print("Fallback: High threat detected based on IoT data and face recognition.")
                actions_executed.append(lock_vehicle())
                actions_executed.append(trigger_vehicle_alarm())
                actions_executed.append(send_alert_email())
            elif (
                face_message == "authorized access detected" and
                iot_data["door_sensor"] == "closed" and
                iot_data["motion_sensor"] == "inactive" and
                fingerprint_status == "authorized"
            ):
                print("Fallback: Low threat detected based on IoT data and face recognition.")
                actions_executed.append(send_alert_email())
            else:
                print("Fallback: Unable to determine threat level. Defaulting to low threat.")
                actions_executed.append(send_alert_email())

        recommended_actions = []

        recommended_actions =  semantic_response['recommended_actions']
        print(f"Recommended actions: {recommended_actions}")

        # DONOT DELETE THIS CODE
        # image_url = asyncio.run(generate_architecture_diagram())
        # print(f"Generated architecture diagram: {image_url}")

        image_url = "architecture_diagram.png"  # Placeholder for the actual image URL

        # Prepare the Response
        response = {
            "faceRecognition": face_message,
            "iotData": iot_data,
            "semanticResponse": semantic_response,
            "threatLevel": threat_level,
            "actions": actions_executed,
            "recommendedActions": recommended_actions,
            "architectureDiagramGenerated": image_url
        }
        return response
    except Exception as e:
        print(f"Error in orchestrate_security: {e}")
        raise RuntimeError(f"Failed to orchestrate security: {e}")