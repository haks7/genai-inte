import os
import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
openai_api_type = "azure"
openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # Azure OpenAI endpoint
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Azure OpenAI API key
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # API version
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Deployment name

# Azure AI Services configuration
ai_services_endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT")
ai_services_key = os.getenv("AZURE_AI_SERVICES_KEY")

# Test Microsoft Foundry AI Project Authentication
try:
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        credential=credential,
        conn_str=os.getenv("AZUREML_CONNECTION_STRING")
    )
    print("Authentication successful!")
except Exception as e:
    print(f"Authentication failed: {e}")


class WeatherAgent:
    def __init__(self, source):
        self.source = source
        self.project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.getenv("AZUREML_CONNECTION_STRING")
        )
        self.agent_id = os.getenv("AZUREML_AGENT_ID")
        self.thread_id = os.getenv("AZUREML_THREAD_ID")

    def make_decision(self, prompt):
        """Use Microsoft Foundry AI Project to make a decision based on a prompt."""
        try:
            # Send the user prompt as a message
            self.project_client.agents.create_message(
                thread_id=self.thread_id,
                role="user",
                content=prompt
            )

            # Process the run
            self.project_client.agents.create_and_process_run(
                thread_id=self.thread_id,
                agent_id=self.agent_id
            )

            # Retrieve the messages
            messages = self.project_client.agents.list_messages(thread_id=self.thread_id)

            # Extract the last message from the assistant
            for text_message in messages.text_messages:
                message_dict = text_message.as_dict()  # Convert to dictionary
                if message_dict.get("type") == "text" and "value" in message_dict.get("text", {}):
                    return message_dict["text"]["value"]  # Extract the response content

            return "No response from the agent."
        except Exception as e:
            print(f"Error using Microsoft Foundry AI Project: {e}")
            return f"Error: Unable to process the decision due to {str(e)}."


class AzureAITextAgent:
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

    def extract_key_phrases(self, text):
        """Extract key phrases using Azure AI Services."""
        url = f"{ai_services_endpoint}/text/analytics/v3.1/keyPhrases"
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
            return result["documents"][0]["keyPhrases"]
        except Exception as e:
            print(f"Error using Azure AI Services for key phrases: {e}")
            return []


def create_weather_agents(weather_data):
    """Create and return weather agents based on the provided weather data."""
    agents = [
        WeatherAgent("TemperatureAgent"),
        WeatherAgent("ConditionAgent")
    ]
    return agents


def read_weather_data_from_storage():
    """Read weather data from a .txt file stored in Azure Storage."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    blob_name = "weather_api.txt"  # File name in Azure Storage

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        # Download and decode the blob data
        blob_data = blob_client.download_blob().readall().decode("utf-8")
        lines = blob_data.strip().split("\n")
        if not lines:
            print("Weather data file is empty.")
            return None

        # Parse the weather data into a dictionary
        weather_data = {}
        for line in lines:
            city, postal_code, temperature, condition = line.split(",")
            weather_data[postal_code.strip()] = {
                "city": city.strip(),
                "temperature": float(temperature.strip()),
                "condition": condition.strip()
            }
        return weather_data
    except Exception as e:
        print(f"Error reading weather data from Azure Storage: {e}")
        return None


def write_results_to_storage(results):
    """Write results to Azure Storage."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    blob_name = "analysis_results.txt"

    print(f"Writing results to storage: {results}")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(results, overwrite=True)
        print("Results successfully written to Azure Storage.")
    except Exception as e:
        print(f"Error writing results to Azure Storage: {e}")