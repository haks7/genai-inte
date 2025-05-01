import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template import PromptTemplateConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch Azure OpenAI credentials from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_MODEL")

# Initialize Semantic Kernel
kernel = Kernel()

# Add Azure OpenAI as the text completion service
service_id = "chat-gpt"
kernel.add_service(
    AzureChatCompletion(
        service_id=service_id,
        deployment_name=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY
    )
)

# Define the request settings
req_settings = kernel.get_prompt_execution_settings_from_service_id(service_id)
req_settings.max_tokens = 2000
req_settings.temperature = 0.7
req_settings.top_p = 0.8

# Define a reusable function for reasoning and decision-making
def create_reasoning_function(prompt_template: str, function_name: str, plugin_name: str):
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
async def run_vehicle_security_reasoning(reasoning_prompt, face_recognition_result, iot_data):
    """
    Run the reasoning function asynchronously for vehicle security scenarios.
    """
    # Validate IoT data
    if not iot_data:
        raise ValueError("IoT data is missing or invalid.")

    # Create the reasoning function dynamically
    reasoning_function = create_reasoning_function(
        prompt_template=reasoning_prompt,
        function_name="vehicle_security_reasoning",
        plugin_name="vehicle_security_plugin",
    )

    # Prepare input for the reasoning function
    input_data = {
        "face_recognition_result": face_recognition_result,
        "door_sensor_status": iot_data.get("door_sensor", "unknown"),
        "motion_sensor_status": iot_data.get("motion_sensor", "unknown"),
    }

    print(f"Input data for vehicle security reasoning: {input_data}")  # Debugging log

    # Invoke the reasoning function
    try:
        result = await kernel.invoke(reasoning_function, input=input_data)
        print(f"Vehicle security reasoning result: {result}")  # Debugging log

        return result
    except Exception as e:
        print(f"Error in vehicle security reasoning function: {e}")
        raise