from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.azure_ai_helper import AzureAITextAgent
from app.azure_cognitive_helper import AzureCognitiveTextAgent
from app.semantic_kernel_helper import run_reasoning
from app.foundry_ai_helper import FoundryAIAgent
import asyncio
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from weather_tool import fetch_weather_data
import utils


routes = Blueprint("routes", __name__)
CORS(routes)  # Enable CORS for cross-origin requests

@routes.route('/api/vehicle-optimization', methods=['POST'])
def vehicle_optimization():
    """Optimize vehicle operations based on weather and user queries."""
    try:
        data = request.get_json()
        print(f"Incoming request data: {data}")  # Debugging log

        user_query = data.get("query", "")
        city = data.get("city", "").strip()  # Accept city
        postal_code = data.get("postalCode", "").strip()  # Accept postal code

        # Validate inputs
        if not user_query or not city or not postal_code:
            return jsonify({"error": "Query, city, and postal code are required"}), 400
        if not city.isalpha():
            return jsonify({"error": "City must contain only alphabetic characters"}), 400
        if not postal_code.isdigit() or len(postal_code) != 4:
            return jsonify({"error": "Postal code must be a 4-digit number"}), 400

        # Combine city and postal code for weather data fetching
        location = f"{city}, {postal_code}"
        print(f"Fetching weather data for location: {location}")  # Debugging log

        # Step 1: Fetch city weather data
        city_weather = fetch_weather_data(location)
        if not city_weather:
            return jsonify({"error": f"Weather data not found for {location}."}), 404

        # Step 2: Analyze sentiment using Azure AI Cognitive Services - Sentiment Text Analytics
        text_sentiment_agent_restapi = AzureAITextAgent("SentimentAnalysis")
        sentiment_analysis = text_sentiment_agent_restapi.analyze_text(user_query)

        # Step 3: Extract key phrases using Azure AI Cognitive Services - Key Phrases Text Analytics
        text_keyphrase_agent_restapi = AzureCognitiveTextAgent("KeyPhraseExtraction")
        key_phrases = text_keyphrase_agent_restapi.extract_key_phrases(user_query)

        # Step 4: Use Foundry AI for decision-making
        foundry_AIProjectClient = FoundryAIAgent("DecisionOnGroundingData")
        foundry_decision = foundry_AIProjectClient.make_decision(user_query, key_phrases, city_weather)
        print(f"Decision: {foundry_decision}")

        # Step 5: Use Semantic Kernel for reasoning
        reasoning_prompt = f"""
        The user query is: {{$input}}.
        The extracted key phrases are: {', '.join(key_phrases)}.
        The weather data is: {{$weather_data}}.
        Provide actionable recommendations for optimizing vehicle operations.
        """
        semantic_response = asyncio.run(run_reasoning(
            reasoning_prompt=reasoning_prompt,
            user_query=user_query,
            key_phrases=key_phrases,
            weather_data=city_weather,
        ))

        # Step 6: Adjust car seat heating
        adjustment = utils.adjust_car_seat_heating(city_weather["temperature"])

        # Return the results as a JSON response
        return jsonify({
            "sentimentAnalysis": f"The sentiment analysis of the query indicates: {sentiment_analysis}.",
            "keyPhrases": f"The key phrases extracted from the query are: {', '.join(key_phrases)}.",
            "decisionmaking": f"The decision based on the query and key phrases is: {foundry_decision}.",
            "semanticResponse": f"The semantic reasoning response is: {semantic_response}.",
            "carSeatAdjustment": f"The car seat adjustment recommendation is: {adjustment}.",
            "cityWeather": city_weather  # From the weather data
        })
    except Exception as e:
        print(f"Error in vehicle_optimization route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500