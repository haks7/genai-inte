import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
from app.face_recognition import recognize_face
from app.iot_simulation import simulate_iot_data
import asyncio

# # Load environment variables from .env file
# load_dotenv()

def send_alert_email():
    """Send an alert email using Gmail."""
    recipient_email = os.getenv("RECIPIENT_EMAIL", "sumana.pinjarla@gmail.com")
    subject = "Vehicle Security Alert"
    body = (
        "Alert! Unauthorized access detected.\n\n"
        "Please take immediate action to secure your vehicle."
    )   
    
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
            return {"action": "Email Sent Successfully", "message": "Email sent successfully."}

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
