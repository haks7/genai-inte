from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

class FoundryAIAgent:
    def __init__(self, source):
        self.source = source
        self.project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.getenv("AZUREML_CONNECTION_STRING")
        )
        self.agent_id = os.getenv("AZUREML_AGENT_ID")
        self.thread_id = os.getenv("AZUREML_THREAD_ID")

    def make_decision(self, prompt, city_weather_data):
        """Use Microsoft Foundry AI Project to make a decision based on a prompt."""
        try:
            # Send the user prompt as a message

            # Optionally attach weather data if supported
            if city_weather_data:
                self.project_client.agents.create_message(
                    thread_id=self.thread_id,
                    role="user",
                    content=prompt,
                #      attachments=[
                #     {
                #         "type": "application/json",
                #         "value": city_weather_data,
                #         "tools": []  # Add an empty tools array if required
                #     }
                # ]
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