from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.azure_ai_helper import AzureAITextAgent
from app.azure_cognitive_helper import AzureCognitiveTextAgent
from app.semantic_kernel_helper import run_reasoning
from app.foundry_ai_helper import FoundryAIAgent
from app.weather_agents import (
    read_weather_data_from_storage,
    adjust_car_seat_heating,
    extract_postal_code,
)
from app.semantic_kernel_helper import run_reasoning
import asyncio



routes = Blueprint("routes", __name__)
CORS(routes)  # Enable CORS for cross-origin requests

@routes.route('/api/vehicle-optimization', methods=['POST'])
def vehicle_optimization():
    """Optimize vehicle operations based on weather and user queries."""
    try:
        data = request.get_json()
        user_query = data.get("query", "")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Step 1: Analyze sentiment using Azure AI Cognitive Services- sentiment Text Analytics
        text_sentiment_agent_restapi = AzureAITextAgent("SentimentAnalysis")
        # Analyze sentiment of the user query
        sentiment_analysis = text_sentiment_agent_restapi.analyze_text(user_query)

        # Step 2: Extract key phrases using Azure AI Cognitive Services - keyPhrases Text Analytics
        text_keyphrase_agent_restapi = AzureCognitiveTextAgent("KeyPhraseExtraction")
        # Extract key phrases from the user query
        key_phrases = text_keyphrase_agent_restapi.extract_key_phrases(user_query)


        # Step 3: Read weather data
        weather_data = read_weather_data_from_storage()
        if not weather_data:
            return jsonify({"error": "No weather data available"}), 500
        
         # Step 4: Extract postal code from key phrases 
        postal_code = extract_postal_code(user_query)
        print(f"Postal code from query: {postal_code}")  # Debugging log
        if not postal_code:
            return jsonify({"error": "Postal code not found in query. Please include a valid 4-digit postal code."}), 400

        # Step 5: Read city weather data
        city_weather = weather_data.get(postal_code)
        if not city_weather:
            return jsonify({"error": "Weather data not found for the provided postal code."}), 404
        

        # Step 6: Use Azure AI Cognitive Services for advanced decision-making but using APIPROJECTCLIENT SDK
        # Initialize the Foundry AI Project client
        # Note: In this case, we are not attaching any weather data to the decision-making process.
        # The decision is based solely on the user query and key phrases.
        # If you want to attach weather data, you can uncomment the relevant lines in the FoundryAIAgent class.
        # Initialize the Foundry AI Project client with the agent ID and thread ID
        # No grounding data or message attachment in this case
        foundry_AIProjectClient = FoundryAIAgent("DecisionOnGroundingData")
        foundry_decision = foundry_AIProjectClient.make_decision(user_query, key_phrases, city_weather)
        print(f"Decision: {foundry_decision}")

        # Step 7: Use Semantic Kernel for reasoning
        # Note: The semantic reasoning process is asynchronous, so we use asyncio.run to execute it.
        # The reasoning process will use the user query, key phrases, and weather data.
        # The reasoning function is defined in the semantic_kernel_helper.py file.
        # The function should be defined to accept the user query, key phrases, and weather data as parameters.
        # The function should return a response based on the reasoning process.
        # The response can be a string or a structured object.

        # Dynamically generate the reasoning prompt
        reasoning_prompt = f"""
        The user query is: {user_query}.
        The extracted key phrases are: {', '.join(key_phrases)}.
        The weather data is: City: {city_weather['city']}, Temperature: {city_weather['temperature']}°C, Condition: {city_weather['condition']}.
        Based on this information, provide actionable recommendations for optimizing vehicle operations.
        """
        # Invoke the reasoning function asynchronously
        semantic_response = asyncio.run(run_reasoning(
        reasoning_prompt=reasoning_prompt,
        user_query=user_query,
        key_phrases=key_phrases,
        weather_data={
            "city": city_weather["city"],
            "temperature": city_weather["temperature"],
            "condition": city_weather["condition"]
            },
            ))         


        # Step 7: Adjust car seat heating
        adjustment = adjust_car_seat_heating(city_weather["temperature"])

        # Return the results as a JSON response
        return jsonify({
        "sentimentAnalysis": f"The sentiment analysis of the query indicates: {sentiment_analysis}.",
        "keyPhrases": f"The key phrases extracted from the query are: {', '.join(key_phrases)}.",
        "decisionmaking": f"The decision based on the query and key phrases is: {foundry_decision}.",
        "semanticResponse": f"The semantic reasoning response is: {semantic_response}.",
        "carSeatAdjustment": f"The car seat adjustment recommendation is: {adjustment}.",
        "cityWeather": city_weather #from the weather data txt file
        })
    except Exception as e:
        print(f"Error in vehicle_optimization route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500