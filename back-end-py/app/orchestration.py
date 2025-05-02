from app.face_recognition import recognize_face
from app.iot_simulation import simulate_iot_data
from app.vehicle_security_kernel import run_vehicle_security_reasoning
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def send_alert_email(subject, body, recipient_email):
    """Send an alert email using Gmail."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    if not sender_email or not sender_password:
        raise ValueError("Email credentials are not set in the environment variables.")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Alert email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def trigger_vehicle_alarm():
    """Simulate triggering a vehicle alarm."""
    print("Vehicle alarm triggered! Beeping sound activated.")
    return {"action": "alarm_triggered", "message": "Vehicle alarm activated."}

def lock_vehicle():
    """Simulate locking the vehicle's engine and wheels."""
    print("Vehicle locked! Engine and wheels are disabled.")
    return {"action": "vehicle_locked", "message": "Vehicle locked. Engine and wheels disabled."}

def orchestrate_security(face_id, door_status, motion_status, fingerprint_status):
    try:
        print("Step 1: Starting face recognition...")
        is_authorized, face_message = recognize_face(face_id)
        print(f"Face recognition result: {face_message}")

        print("Step 2: Simulating IoT data...")
        iot_data = simulate_iot_data(door_status, motion_status, fingerprint_status)  # Pass fingerprint_status
        print(f"IoT data: {iot_data}")
        
        print("Step 3: Running Semantic Kernel reasoning...")
        reasoning_prompt = f"""
        The vehicle is experiencing the following conditions:
        - Face recognition result: {{face_recognition_result}}.
        - Door sensor status: {{door_sensor_status}}.
        - Motion sensor status: {{motion_sensor_status}}.
        - Fingerprint status: {{fingerprint_status}}.

        Based on the above conditions:
        - If the face recognition result is "Unauthorized access detected" or the door sensor status is "forced_open" or the motion sensor status is "active" or the fingerprint status is "unauthorized", classify the threat level as "high" and recommend immediate actions to secure the vehicle.
        - If the face recognition result is "Authorized access" and all other sensor statuses indicate no suspicious activity, classify the threat level as "low".
        - If the face recognition result is inconclusive or unknown, or if there is some suspicious activity but no immediate danger, classify the threat level as "medium".

        Provide the following:
        1. The threat level ("low", "medium", or "high").
        2. A list of actions to take based on the threat level.
        """
        try:
            semantic_response = asyncio.run(run_vehicle_security_reasoning(
                reasoning_prompt=reasoning_prompt,
                face_recognition_result=face_message,
                iot_data=iot_data,
                fingerprint_status=fingerprint_status
            ))
            print(f"Semantic Kernel response: {semantic_response}")
        except Exception as e:
            print(f"Error in Semantic Kernel reasoning: {e}")
            semantic_response = {
                "threat_level": "low",  # Default to "low" if reasoning fails
                "actions": []
            }

        # Fallback logic for incorrect responses
        if semantic_response["threat_level"] == "low" and (
            face_message == "Unauthorized access detected" or
            iot_data["door_sensor"] == "forced_open" or
            iot_data["motion_sensor"] == "active" or
            fingerprint_status == "unauthorized"
        ):
            print("Fallback: Adjusting threat level to 'high' due to suspicious activity.")
            semantic_response["threat_level"] = "high"
            semantic_response["actions"] = ["lock_vehicle", "send_email"]

        # Parse the Semantic Kernel response
        threat_level = semantic_response.get("threat_level", "low")
        actions = semantic_response.get("actions", [])

        # Prepare the response to send back to the front end
        response = {
            "faceRecognition": face_message,
            "iotData": iot_data,
            "semanticResponse": semantic_response,
            "threatLevel": threat_level,
            "actionsExecuted": []
        }

        # Execute actions based on the Semantic Kernel response
        for action in actions:
            if action == "lock_vehicle":
                lock_response = lock_vehicle()
                response["actionsExecuted"].append(lock_response)
            elif action == "trigger_alarm":
                alarm_response = trigger_vehicle_alarm()
                response["actionsExecuted"].append(alarm_response)
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

        # Handle cases where no actions are required
        if not response["actionsExecuted"]:
            response["actionsExecuted"].append({"action": "none", "message": "No immediate action required."})

        return response
    except Exception as e:
        print(f"Error in orchestrate_security: {e}")
        raise


# 1. Orchestration Overview
# The orchestrate_security function integrates multiple components to secure a vehicle based on various inputs. Here's the flow:

# Face Recognition:

# Uses recognize_face to determine if the face is authorized or unauthorized.
# This is a binary decision-making step.
# IoT Data Simulation:

# Uses simulate_iot_data to simulate the status of IoT sensors (door, motion, fingerprint).
# This provides additional context for decision-making.
# Semantic Kernel Reasoning:

# Combines the face recognition result and IoT data into a reasoning prompt.
# The Semantic Kernel processes this prompt to classify the threat level (low, medium, high) and recommend actions (e.g., lock vehicle, send email).
# This step introduces contextual reasoning and decision-making capabilities.
# Action Execution:

# Based on the Semantic Kernel's response, actions like locking the vehicle, triggering an alarm, or sending an email are executed.
# Fallback Logic:

# If the Semantic Kernel response is incorrect or incomplete, fallback logic adjusts the threat level and actions based on predefined rules.