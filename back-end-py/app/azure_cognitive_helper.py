import requests
import os

class AzureCognitiveTextAgent:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT") + "/text/analytics/v3.1/keyPhrases"
        self.key = os.getenv("AZURE_AI_SERVICES_KEY")

    def extract_key_phrases(self, text):
        """Extract key phrases using Azure Text Analytics REST API."""
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }
        payload = {
            "documents": [
                {"id": "1", "language": "en", "text": text}
            ]
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["documents"][0]["keyPhrases"]
        except Exception as e:
            print(f"Error extracting key phrases: {e}")
            return []