import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AZURE_GPT_TEXT_IMAGE_ENDPOINT = os.getenv("AZURE_GPT_TEXT_IMAGE_ENDPOINT")
AZURE_GPT_TEXT_IMAGE_KEY = os.getenv("AZURE_GPT_TEXT_IMAGE_KEY")

def generate_architecture_diagram():
    """
    Generate an architecture diagram using Azure OpenAI's gpt-image-1 deployment.
    """
    if not AZURE_GPT_TEXT_IMAGE_ENDPOINT or not AZURE_GPT_TEXT_IMAGE_KEY:
        raise EnvironmentError("Missing required Azure GPT Text-to-Image credentials in environment variables.")

    prompt = (
        "Generate an architecture diagram for a Vehicle Security System. "
        "The system includes the following components: "
        "1. IoT Hub to collect data from sensors (door status, motion status, fingerprint status). "
        "2. Semantic Response powered by Chat-GPT to analyze the data and determine the threat level. "
        "3. GPT-Image-1 to generate architecture diagrams based on the system's state. "
        "Outputs include vehicle locking, trigger_vehicle_alarm, and email alerts triggered by the threat level determined by Semantic Response. "
        "Show the flow of data between these components and highlight the decision-making process."
    )

    # Define the request payload
    payload = {
        "prompt": prompt,
        "size": "1024x1024",  # Medium size
        "quality": "medium",  # Medium quality
        "output_compression": 100,
        "output_format": "png",
        "n": 1  # Number of images to generate
    }

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_GPT_TEXT_IMAGE_KEY}"
    }

    try:
        # Make the POST request to the Azure OpenAI endpoint
        response = requests.post(AZURE_GPT_TEXT_IMAGE_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response
        result = response.json()
        if "data" in result and len(result["data"]) > 0:
            # Decode the base64 image data
            image_base64 = result["data"][0]["b64_json"]
            image_data = base64.b64decode(image_base64)

            # Save the image to a file
            with open("architecture_diagram.png", "wb") as image_file:
                image_file.write(image_data)

            print("Architecture diagram generated and saved as 'architecture_diagram.png'.")
            return "architecture_diagram.png"
        else:
            print("No image data found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error in generating architecture diagram: {e}")
        raise RuntimeError(f"Failed to generate architecture diagram: {e}")
