import asyncio
from flask import jsonify
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template import PromptTemplateConfig
# from dotenv import load_dotenv
import os

# # Load environment variables from .env file
# load_dotenv()

# Fetch Azure OpenAI credentials from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Validate that all required environment variables are set
if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
    raise EnvironmentError("Missing required Azure OpenAI credentials in environment variables.")

# Initialize Semantic Kernel
def create_kernel() -> Kernel:
    """
    Creates and initializes the Semantic Kernel with Azure OpenAI settings.
    """
    kernel = Kernel()
    azure_openai_client = AzureChatCompletion(
        service_id="chat-gpt",
        deployment_name="gpt-35-turbo",
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY
    )
    kernel.add_service(azure_openai_client)
    return kernel

# Create the kernel instance
kernel = create_kernel()

# Define a reusable function for reasoning and decision-making
def create_reasoning_function(prompt_template: str, function_name: str, plugin_name: str):
    """
    Creates a reasoning function dynamically using a prompt template.
    """
    req_settings = kernel.get_prompt_execution_settings_from_service_id("chat-gpt")
    req_settings.max_tokens = 2000
    req_settings.temperature = 0.7
    req_settings.top_p = 0.8

    prompt_template_config = PromptTemplateConfig(
        template=prompt_template,
        name=function_name,
        template_format="semantic-kernel",
        execution_settings=req_settings,
    )
    return kernel.add_function(
        function_name=function_name,
        plugin_name=plugin_name,
        prompt_template_config=prompt_template_config,
    )

# Define a function to run vehicle security reasoning
async def run_vehicle_security_reasoning(reasoning_prompt: str, face_recognition_result: str, iot_data: dict, fingerprint_status: str):
    """
    Run the reasoning function asynchronously for vehicle security scenarios.
    """
    if not iot_data:
        raise ValueError("IoT data is missing or invalid.")

    # Create the reasoning function dynamically
    reasoning_function = create_reasoning_function(
        prompt_template=reasoning_prompt,
        function_name="vehicle_security_reasoning",
        plugin_name="vehicle_security_plugin",
    )

    # Prepare input data for the reasoning function
    input_data = {
        "face_recognition_result": face_recognition_result,
        "door_sensor_status": iot_data.get("door_sensor", "unknown"),
        "motion_sensor_status": iot_data.get("motion_sensor", "unknown"),
        "fingerprint_status": fingerprint_status
    }

    print(f"Input data for vehicle security reasoning: {input_data}")  # Debugging log

    try:
        # Invoke the reasoning function
        result = await kernel.invoke(reasoning_function, input=input_data)
        print(f"Raw Semantic Kernel response: {result}")  # Debugging log

        return result
    except Exception as e:
        print(f"Error in vehicle security reasoning function: {e}")
        raise RuntimeError(f"Failed to execute vehicle security reasoning: {e}")