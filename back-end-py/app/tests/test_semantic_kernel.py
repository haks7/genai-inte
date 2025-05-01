import asyncio
from semantic_kernel_helper import run_reasoning

async def main():
    # Example input data
    user_query = "What is the weather like in Melbourne? Should I turn on the car seat heating?"
    key_phrases = ["weather", "Melbourne", "car seat heating"]
    city_or_postal_code = "3000"  # Example postal code

    # Generate reasoning prompt
    reasoning_prompt = f"""
    The user query is: {{$input}}.
    The extracted key phrases are: {', '.join(key_phrases)}.
    The weather data is: {{$weather_data}}.
    Provide actionable recommendations for optimizing vehicle operations.
    """

    print(f"Input data for reasoning: {user_query}, {key_phrases}, {city_or_postal_code}")  # Debugging log
    print(f"Reasoning prompt: {reasoning_prompt}")  # Debugging log

    # Run the reasoning function
    try:
        semantic_response = await run_reasoning(
            reasoning_prompt=reasoning_prompt,
            user_query=user_query,
            key_phrases=key_phrases,
            city_or_postal_code=city_or_postal_code,
        )
        print(f"Reasoning Result: {semantic_response}")
    except Exception as e:
        print(f"Error during reasoning: {e}")

# Run the test
if __name__ == "__main__":
    asyncio.run(main())