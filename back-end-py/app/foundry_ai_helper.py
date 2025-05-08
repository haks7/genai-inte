from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

class FoundryAIAgent:
    def __init__(self, source):
        """Initialize the Foundry AI Agent with required configurations."""
        self.source = source
        self.project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.getenv("AZUREML_CONNECTION_STRING")
        )
        self.agent_id = os.getenv("AZUREML_AGENT_ID")
        self.thread_id = os.getenv("AZUREML_THREAD_ID")

    def make_decision(self, prompt, key_phrases, city_weather):
        """Use Microsoft Foundry AI Project to make a decision based on user query and key phrases."""
        try:
            # Combine the user query and key phrases into a single message
            combined_prompt = f"{prompt}\nKey Phrases: {', '.join(key_phrases)}"
            combined_prompt += f"\nCity Weather: {city_weather}"

            # Send the combined prompt as a message
            self.project_client.agents.create_message(
                thread_id=self.thread_id,
                role="user",
                content=combined_prompt
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
        
    def send_prompt(self, prompt):
        """
        Send a prompt to the Foundry Agent and retrieve the response.
        """
        try:
            # Get the thread and agent
            thread = self.project_client.agents.get_thread(self.thread_id)
            agent = self.project_client.agents.get_agent(self.agent_id)

            # Create a message in the thread
            self.project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=prompt
            )

            # Process the run
            self.project_client.agents.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent.id
            )

            # Retrieve messages from the thread
            messages = self.project_client.agents.list_messages(thread_id=thread.id)

            # Extract and return the assistant's response
            for text_message in messages.text_messages:
                message_dict = text_message.as_dict()
                if message_dict.get("type") == "text" and "value" in message_dict.get("text", {}):
                    return message_dict["text"]["value"]

            return "No response from the agent."
        except Exception as e:
            print(f"Error sending prompt to Agent: {e}")
            return f"Error: Unable to process the prompt due to {str(e)}."

# When to Use Each Approach
# Use AIProjectClient When:
    # You need to manage workflows involving multiple AI agents.
    # You want to attach additional data (e.g., weather data) to prompts for context-aware decision-making.
    # You are working with Foundry AI or other project-based Azure AI services.
# Use REST API for Text Analytics When:
    # You need to perform specific text analysis tasks, such as sentiment analysis or key phrase extraction.
    # You want a lightweight and straightforward integration for analyzing text.
    # You do not need to manage threads or workflows.