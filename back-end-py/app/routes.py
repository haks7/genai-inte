from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.semantic_kernel_helper import run_reasoning
from app.azure_ai_helper import AzureAITextAgent
from app.azure_cognitive_helper import AzureCognitiveTextAgent
from app.utils import (
    adjust_car_seat_heating,
    fetch_calendar_events,
    simulate_driver_fatigue,
    suggest_stopovers,
    prepare_vehicle_ambience,
    fetch_charging_stations,
)
from app.foundry_ai_helper import FoundryAIAgent
import asyncio
from app.weather_tool import fetch_weather_data

routes = Blueprint("routes", __name__)
CORS(routes)  # Enable CORS for cross-origin requests

@routes.route('/api/vehicle-optimization', methods=['POST'])
def vehicle_optimization():
    """
    Optimize vehicle operations based on the owner's agenda, preferences, and contextual factors.
    """
    try:
        # Step 1: Parse user inputs
        data = request.get_json() or {}
        print(f"Incoming request data: {data}")  # Debugging log

        # Default values for inputs
        user_query = data.get("query", "").strip() or "Plan my trip efficiently."
        city = data.get("city", "").strip() or "Melbourne"
        country = data.get("country", "").strip() or "Australia"
        postal_code = data.get("postalCode", "").strip() or "3000"
        vehicle_status = data.get("vehicleStatus") or {"batteryLevel": 80}  # Simulated vehicle status
        preferences = data.get("preferences") or {"food": "vegan", "music": "jazz"}  # Simulated preferences

        # Combine location for weather data fetching
        location = f"{city}, {country}"
        if postal_code:
            location += f", {postal_code}"
        print(f"Fetching weather data for location: {location}")  # Debugging log

        # Step 2: Fetch city weather data
        city_weather = fetch_weather_data(location) or {"temperature": 22, "condition": "Clear"}  # Simulated fallback
        print(f"Weather data: {city_weather}")

        # Step 3: Sync with the owner's calendar
        calendar_events = fetch_calendar_events()
        print(f"Calendar events: {calendar_events}")

        # Step 4: Analyze sentiment and extract key phrases
        azure_ai_agent = AzureAITextAgent("SentimentAnalysis")
        sentiment_analysis = azure_ai_agent.analyze_sentiment(user_query)
        if not sentiment_analysis:
            raise ValueError("Sentiment analysis failed.")
        
        azure_ai_cognitive_agent = AzureCognitiveTextAgent("KeyPhraseExtraction")
        key_phrases = azure_ai_cognitive_agent.extract_key_phrases(user_query)
        if not key_phrases:
            raise ValueError("Key phrase extraction failed.")
        

        # Step 5: Use Foundry AI for decision-making
        foundry_agent = FoundryAIAgent("DecisionOnGroundingData")
        foundry_decision = foundry_agent.make_decision(user_query, key_phrases, city_weather)
        if not foundry_decision:
            raise ValueError("Foundry decision-making failed.")
        # Simulate decision-making process
        print(f"Foundry decision: {foundry_decision}")

        # Step 6: Plan the route based on contextual factors
        charging_stations = fetch_charging_stations(location, vehicle_status["batteryLevel"])
        stopover_suggestions = suggest_stopovers(calendar_events, preferences)
        route_plan = {
            "route": "Energy-efficient Route A",
            "chargingStops": charging_stations,
            "stopovers": stopover_suggestions,
        }
        print(f"Route plan: {route_plan}")

        # Step 7: Prepare the car before departure
        car_preparation = prepare_vehicle_ambience(preferences, city_weather)
        print(f"Car preparation: {car_preparation}")

        # Step 8: Detect driver fatigue and suggest rest stops
        fatigue_detected = simulate_driver_fatigue(vehicle_status)
        rest_stop_suggestion = (
            "Driver fatigue detected. Suggesting a rest stop nearby."
            if fatigue_detected
            else "No fatigue detected. Continuing the trip."
        )
        print(f"Rest stop suggestion: {rest_stop_suggestion}")

        # Step 9: Adjust car seat heating
        adjustment = adjust_car_seat_heating(city_weather["temperature"], foundry_decision)
        print(f"Car seat adjustment: {adjustment}")

        # Step 10: Use Semantic Kernel for reasoning
        reasoning_prompt = f"""
        The user query is: {user_query}.
        The extracted key phrases are: {', '.join(key_phrases)}.
        The weather data is: {city_weather}.
        Provide actionable recommendations for optimizing vehicle operations.
        """
        semantic_response = asyncio.run(run_reasoning(
            reasoning_prompt=reasoning_prompt,
            user_query=user_query,
            key_phrases=key_phrases,
            weather_data=city_weather,
        ))
        print(f"Semantic reasoning response: {semantic_response}")

        # Step 11: Prepare trip summary and notifications
        trip_summary = {
            "estimatedArrivalTime": "10:30 AM",
            "routeDetails": route_plan["route"],
            "energyConsumptionPlan": "Charge at Station B for 20 minutes.",
        }

        # Return the results as a JSON response
        return jsonify({
            "sentimentAnalysis": f"The sentiment analysis of the query indicates: {sentiment_analysis}.",
            "keyPhrases": f"The key phrases extracted from the query are: {', '.join(key_phrases)}.",
            "decisionmaking": f"The decision based on the query and key phrases is: {foundry_decision}.",
            "semanticResponse": f"The semantic reasoning response is: {semantic_response}.",
            "carSeatHeatAdjustment": f"The car seat heat adjustment recommendation is: {adjustment}.",
            "routePlan": route_plan,
            "carPreparation": car_preparation,
            "restStopSuggestion": rest_stop_suggestion,
            "tripSummary": trip_summary,
            "cityWeather": city_weather  # From the weather data
        })
    except Exception as e:
        print(f"Error in vehicle_optimization route: {e}")
        return jsonify({"error": "Internal Server Error"}), 500