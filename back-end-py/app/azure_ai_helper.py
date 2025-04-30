import openai
import os

import requests

# Azure AI Services configuration
ai_services_endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT")
ai_services_key = os.getenv("AZURE_AI_SERVICES_KEY")

class AzureAITextAgent:
    def __init__(self):
        # Set global OpenAI configuration for Azure
        openai.api_type = "azure"
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    def analyze_text(self, text):
        """Analyze text using Azure AI Services."""
        url = f"{ai_services_endpoint}/text/analytics/v3.1/sentiment"
        headers = {
            "Ocp-Apim-Subscription-Key": ai_services_key,
            "Content-Type": "application/json"
        }
        payload = {
            "documents": [
                {"id": "1", "language": "en", "text": text}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["documents"][0]
        except Exception as e:
            print(f"Error using Azure AI Services: {e}")
            return None