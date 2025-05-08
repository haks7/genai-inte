from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.azure_ai_helper import AzureAITextAgent
from app.azure_cognitive_helper import AzureCognitiveTextAgent
from app.utils import (
    adjust_car_seat_heating,
    fetch_calendar_events,
    prepare_vehicle_ambience,
)
from app.foundry_ai_helper import FoundryAIAgent
from app.weather_tool import fetch_weather_data

routes = Blueprint("routes", __name__)
CORS(routes)

@routes.route('/api/vehicle-optimization', methods=['POST'])
def vehicle_optimization():
    """
    Optimize vehicle operations based on the owner's agenda, preferences, and contextual factors.
    """
    try:
        # Log headers and raw data for debugging
        print(f"Request headers: {request.headers}")
        print(f"Raw request data: {request.data}")

        # Parse input data
        user_query = request.form.get("query", "Should I switch on car seat heat?").strip()
        user_query += " Ensure to provide whether car seat heat adjustment is needed or not."
        city = request.form.get("city", "Melbourne").strip()
        country = request.form.get("country", "Australia").strip()
        postal_code = request.form.get("postalCode", "3000").strip()

        preferences = {"food": "vegan", "music": "calm"}  # Simulated preferences

        # Step 1: Fetch calendar events
        calendar_events = fetch_calendar_events()

        # Step 2: Fetch weather data
        location = f"{city}, {country}, {postal_code}".strip(", ")
        city_weather = fetch_weather_data(location) or {"temperature": 22, "condition": "Clear"}  # Fallback

        # Step 3: Analyze sentiment
        azure_ai_agent = AzureAITextAgent("SentimentAnalysis")
        sentiment_analysis = azure_ai_agent.analyze_sentiment(user_query)
        if not sentiment_analysis:
            raise ValueError("Sentiment analysis failed.")

        # Step 4: Extract key phrases
        azure_ai_cognitive_agent = AzureCognitiveTextAgent("KeyPhraseExtraction")
        key_phrases = azure_ai_cognitive_agent.extract_key_phrases(user_query)
        if not key_phrases:
            raise ValueError("Key phrase extraction failed.")

        # Step 5: Decision-making with Foundry AI
        foundry_agent = FoundryAIAgent("DecisionOnGroundingData")
        foundry_decision = foundry_agent.make_decision(user_query, key_phrases, city_weather)

        # Step 6: Generate stopover suggestions
        stopover_prompt = f"""
        Based on the following calendar events and preferences, suggest suitable stopovers in string format only:
        Calendar Events: {calendar_events}
        Preferences: {preferences}
        """
        stopover_suggestions = foundry_agent.send_prompt(stopover_prompt)

        # Step 7: Generate route plan
        route_prompt = f"""
        Based on the following details, suggest an energy-efficient route plan in string format only:
        - Location: {location}
        - Preferences: {preferences}
        """
        route_plan = foundry_agent.send_prompt(route_prompt)

        # Step 8: Prepare the car
        car_preparation = prepare_vehicle_ambience(preferences, city_weather)

        # Step 9: Adjust car seat heating
        adjustment = adjust_car_seat_heating(city_weather["temperature"], foundry_decision)

        # Prepare the response
        response = {
            "sentimentAnalysis": f"The sentiment analysis of the query indicates: {sentiment_analysis}.",
            "keyPhrases": f"The key phrases extracted from the query are: {', '.join(key_phrases)}.",
            "decisionmaking": f"The decision based on the query and key phrases is: {foundry_decision}.",
            "carSeatHeatAdjustment": f"The car seat heat adjustment recommendation is: {adjustment}.",
            "routePlan": route_plan,
            "carPreparation": car_preparation,
            "restStopSuggestion": stopover_suggestions,
            "cityWeather": city_weather,
        }

        # Log the response before sending it to the client
        print(f"Response to client: {response}")

        return jsonify(response)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Internal Server Error"}), 500