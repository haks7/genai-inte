import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.prompt_template import PromptTemplateConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch Azure OpenAI credentials from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_MODEL_ID = "Agent995" 
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize Semantic Kernel
kernel = Kernel()

# Add Azure OpenAI as the text completion service
service_id = "chat-gpt"
kernel.add_service(
    OpenAIChatCompletion(
        service_id=service_id,
        api_key=AZURE_OPENAI_API_KEY,
        ai_model_id=AZURE_OPENAI_MODEL_ID,)
)

# Define the request settings
req_settings = kernel.get_prompt_execution_settings_from_service_id(service_id)
req_settings.max_tokens = 50
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

# Example prompt for reasoning
reasoning_prompt = """
The user query is: {{$input}}.
The extracted key phrases are: {{$key_phrases}}.
The weather data is: {{$weather_data}}.
Provide actionable recommendations for optimizing vehicle operations.
"""

reasoning_function = create_reasoning_function(
    prompt_template=reasoning_prompt,
    function_name="reasoning_function",
    plugin_name="vehicle_optimization_plugin",
)

async def run_reasoning(user_query, key_phrases, weather_data):
    """Run the reasoning function asynchronously."""
    try:
        input_data = {
            "input": user_query,
            "key_phrases": ", ".join(key_phrases),  # Convert list to string
            "weather_data": f"City: {weather_data['city']}, Temperature: {weather_data['temperature']}°C, Condition: {weather_data['condition']}"
        }
        print(f"Input data for reasoning: {input_data}")  # Debugging log
        result = await kernel.invoke(reasoning_function)#, input=input_data)
        return result
    except Exception as e:
        print(f"Error in run_reasoning: {e}")
        raise

# Uncomment this block for testing purposes
# if __name__ == "__main__":
#     asyncio.run(run_reasoning(
#         user_query="What is the weather like in Melbourne? Should I turn on the car seat heating?",
#         key_phrases=["weather", "Melbourne", "car seat heating"],
#         weather_data={
#             "city": "Melbourne",
#             "temperature": 15,
#             "condition": "Sunny"
#         }
#     ))