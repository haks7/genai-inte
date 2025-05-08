import aiohttp
import asyncio
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AZURE_GPT_TEXT_IMAGE_ENDPOINT = os.getenv("AZURE_OPENAI_IMAGE_GENERATION_ENDPOINT")
AZURE_GPT_TEXT_IMAGE_KEY = os.getenv("AZURE_OPENAI_IMAGE_GENERATION_KEY")

async def generate_architecture_diagram(face_recognition_result, iot_data, fingerprint_status):
    """
    Generate an architecture diagram using Azure OpenAI's gpt-image-1 deployment.
    """
    if not AZURE_GPT_TEXT_IMAGE_ENDPOINT or not AZURE_GPT_TEXT_IMAGE_KEY:
        raise EnvironmentError("Missing required Azure GPT Text-to-Image credentials in environment variables.")
    
    # Prepare input data for the reasoning function
    input_data = {
        "face_recognition_result": face_recognition_result,
        "door_sensor_status": iot_data.get("door_sensor", "unknown"),
        "motion_sensor_status": iot_data.get("motion_sensor", "unknown"),
        "fingerprint_status": fingerprint_status
    }

    prompt = (
        "Generate an architecture diagram for a Vehicle Security System. "
        "The system includes the following components: "
       generate_architecture_diagram
        "3. GPT-Image-1 to generate architecture diagrams based on the system's state. "
        "Outputs include vehicle locking, trigger_vehicle_alarm, and email alerts triggered by the threat level determined by Semantic Response. "
        "Show the flow of data between these components and highlight the decision-making process."
    )

    payload = {
        "prompt": prompt,
        "size": "1024x1024",  # Medium size
        "quality": "medium",  # Medium quality
        "output_compression": 100,
        "output_format": "png",
        "n": 1  # Number of images to generate
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_GPT_TEXT_IMAGE_KEY}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(AZURE_GPT_TEXT_IMAGE_ENDPOINT, json=payload, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()

                if "data" in result and len(result["data"]) > 0:
                    image_base64 = result["data"][0]["b64_json"]
                    image_data = base64.b64decode(image_base64)

                    with open("architecture_diagram.png", "wb") as image_file:
                        image_file.write(image_data)

                    print("Architecture diagram generated and saved as 'architecture_diagram.png'.")
                    return "architecture_diagram.png"
                else:
                    print("No image data found in the response.")
                    return None
    except aiohttp.ClientError as e:
        print(f"Error in generating architecture diagram: {e}")
        raise RuntimeError(f"Failed to generate architecture diagram: {e}")