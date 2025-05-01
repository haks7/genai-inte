import asyncio
from semantic_kernel_helper import run_reasoning

async def main():
    

    # Example input data
    user_query = "What is the weather like in Melbourne? Should I turn on the car seat heating?"
    key_phrases = ["weather", "Melbourne", "car seat heating"]
    weather_data = {
        "city": "Melbourne",
        "temperature": 15,
        "condition": "Sunny"
    }

    # Define the reasoning prompt
    reasoning_prompt = """
    The user query is: {{$user_query}}.
    The extracted key phrases are: {{$key_phrases}}.
    The weather data is: {{$weather_data}}.
    Provide actionable recommendations for optimizing vehicle operations.
    """

    print(f"Input data for reasoning: {user_query}, {key_phrases}, {weather_data}")  # Debugging log
    print(f"Reasoning prompt: {reasoning_prompt}")  # Debugging log
    
    # Run the reasoning function
    try:
        result = await run_reasoning(reasoning_prompt, user_query, key_phrases, weather_data)
        print(f"Reasoning Result: {result}")
    except Exception as e:
        print(f"Error during reasoning: {e}")

# Run the test
if __name__ == "__main__":
    asyncio.run(main())