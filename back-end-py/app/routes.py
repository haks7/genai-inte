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

        # Step 1: Analyze sentiment using Azure OpenAI
        text_agent = AzureAITextAgent()
        sentiment_analysis = text_agent.analyze_text(user_query)

        # Step 2: Extract key phrases using Azure Cognitive Services
        cognitive_agent = AzureCognitiveTextAgent()
        key_phrases = cognitive_agent.extract_key_phrases(user_query)

        # Step 3: Extract postal code from key phrases
        postal_code = extract_postal_code(user_query)
        print(f"Postal code from query: {postal_code}")  # Debugging log
        if not postal_code:
            return jsonify({"error": "Postal code not found in query. Please include a valid 4-digit postal code."}), 400

        # Step 4: Read weather data
        weather_data = read_weather_data_from_storage()
        if not weather_data:
            return jsonify({"error": "No weather data available"}), 500
        
        print(f"Weather data: {weather_data}")  # Debugging log
        if postal_code not in weather_data:
            return jsonify({"error": f"No weather data available for postal code {postal_code}"}), 404


        city_weather = weather_data[postal_code]
        print(f"City weather data: {city_weather}")  # Debugging log


        # # Step 5: Use Semantic Kernel for reasoning
        # semantic_response = asyncio.run(run_reasoning(
        #     user_query=user_query,
        #     key_phrases=key_phrases,
        #     weather_data=city_weather,
        # ))
        semantic_response = ""

        # Step 6: Use Foundry AI for advanced decision-making
        foundry_agent = FoundryAIAgent("TemperatureAgent")
        foundry_decision = foundry_agent.make_decision(user_query, city_weather)
        print(f"Decision: {foundry_decision}")


        # Step 7: Adjust car seat heating
        adjustment = adjust_car_seat_heating(city_weather["temperature"])

        # Return the results
        return jsonify({
            "sentimentAnalysis": sentiment_analysis,
            "keyPhrases": key_phrases,
            "semanticResponse": semantic_response,
            "foundryDecision": foundry_decision,
            "carSeatAdjustment": adjustment,
            "cityWeather": city_weather,
        })
    except Exception as e:
        print(f"Error in vehicle_optimization route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500