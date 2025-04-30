import os
import re
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from weather_agents import (
    create_weather_agents,
    read_weather_data_from_storage,
    write_results_to_storage,
    AzureAITextAgent,
)

import openai
from waitress import serve
import requests

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Azure AI Services configuration
ai_services_endpoint = os.getenv("AZURE_AI_SERVICES_ENDPOINT")
ai_services_key = os.getenv("AZURE_AI_SERVICES_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


def adjust_car_seat_heating(temperature):
    """Adjust the car seat heating system based on temperature."""
    if temperature < 10:
        print("Temperature is low. Turning on seat heating.")
        return "Heating ON"
    elif 10 <= temperature <= 25:
        print("Temperature is moderate. Keeping seat heating off.")
        return "Heating OFF"
    else:
        print("Temperature is high. Ensuring seat cooling is active.")
        return "Cooling ON"

# Extract postal code from the user query
def extract_postal_code(query):
    """Extract postal code from the user query."""
    match = re.search(r'\b\d{4}\b', query)  # Matches a 4-digit postal code
    return match.group(0) if match else None

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle weather-related queries from the frontend."""
    # Parse the JSON payload from the request
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Analyze the text input using Azure AI Services
    text_agent = AzureAITextAgent()
    sentiment_analysis = text_agent.analyze_text(user_query)
    if not sentiment_analysis:
        sentiment_analysis = {
            "sentiment": "neutral",
            "confidenceScores": {"positive": 0.0, "neutral": 1.0, "negative": 0.0},
            "sentences": [],
            "warnings": []
        }
        print("Sentiment analysis failed. Defaulting to neutral sentiment.")
    print(f"Text Analysis: {sentiment_analysis}")

    # Extract key phrases from the user query
    key_phrases = text_agent.extract_key_phrases(user_query)
    print(f"Key Phrases: {key_phrases}")

    # Read weather data from Azure Storage
    weather_data = read_weather_data_from_storage()
    if not weather_data:
        print("Weather data could not be loaded.")
        return jsonify({"error": "No weather data available"}), 500

    print(f"Weather data loaded: {weather_data}")

    # Extract postal code from the user query
    postal_code = extract_postal_code(user_query)
    if not postal_code:
        return jsonify({"error": "Postal code not found in query. Please include a valid 4-digit postal code."}), 400

    if postal_code not in weather_data:
        return jsonify({"error": f"No weather data available for postal code {postal_code}"}), 404

    # Get weather data for the specified postal code
    city_weather = weather_data[postal_code]
    print(f"Weather data for {city_weather['city']} ({postal_code}): {city_weather}")

    # Generate a sentiment-based response
    city_name = city_weather["city"]
    if sentiment_analysis["sentiment"] == "negative":
        sentiment_response = f"I'm sorry to hear that you're unhappy. Here's the weather update for {city_name}."
    elif sentiment_analysis["sentiment"] == "positive":
        if "love" in user_query.lower():
            sentiment_response = f"I'm glad you love the weather! Here's the weather update for {city_name}."
        else:
            sentiment_response = f"Great! Here's the weather update for {city_name}."
    else:
        sentiment_response = f"Here's the weather update for {city_name}."

    # Create agents and make decisions
    agents = create_weather_agents(city_weather)
    decisions = []
    for agent in agents:
        decision_prompt = (
            f"The user query is: {user_query}. "
            f"The weather data is: {city_weather}. "
            f"Provide a clear and actionable recommendation based on this information."
        )
        decision = agent.make_decision(decision_prompt)
        if not decision or decision.startswith("Error"):
            decision = f"No decision could be made by {agent.source}."
        decisions.append(f"Decision by {agent.source}: {decision}")
        print(f"Decision by {agent.source}: {decision}")

    # Adjust car seat heating based on temperature
    temperature = city_weather["temperature"]
    print(f"Temperature for car seat adjustment: {temperature}")
    adjustment = adjust_car_seat_heating(temperature)
    print(f"Car seat adjustment: {adjustment}")

    # Store results in Azure Storage
    results = f"User Query: {user_query}\nSentiment Analysis: {sentiment_analysis}\nDecisions: {decisions}\nCar Seat Adjustment: {adjustment}"
    print(f"Results to be written to storage: {results}")
    write_results_to_storage(results)
    print("Results stored in Azure Storage.")

    # Return the results as a JSON response
    return jsonify({
        "sentimentAnalysis": sentiment_analysis,
        "sentimentResponse": sentiment_response,
        "decisions": decisions,
        "carSeatAdjustment": adjustment
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))