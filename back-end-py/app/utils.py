import re
import requests
from app.foundry_ai_helper import FoundryAIAgent
import os

def adjust_car_seat_heating(temperature, foundry_decision):
    """Adjust car seat heating based on temperature and Foundry decision."""
    # Normalize the decision to lowercase for easier keyword matching
    decision_lower = foundry_decision.lower()

    # Default to relying on temperature if the decision is unclear
    if "increase heating" in decision_lower or "too cold" in decision_lower or temperature < 10:
        return "Increase seat heating to high." if temperature < 10 else "Increase seat heating to medium."
    elif "decrease heating" in decision_lower or "too warm" in decision_lower or temperature > 25:
        return "Decrease seat heating to low."
    elif "no adjustment" in decision_lower or "optimal" in decision_lower:
        return "No adjustment needed based on Foundry decision."
    else:
        # Default case: rely on temperature
        return (
            "Increase seat heating to high based on temperature." if temperature < 10 else
            "Increase seat heating to medium based on temperature." if 10 <= temperature < 20 else
            "Decrease seat heating to low based on temperature." if temperature > 25 else
            "No heating adjustment needed based on temperature."
        )

def extract_postal_code(query):
    """Extract postal code from the user query."""
    match = re.search(r'\b\d{4}\b', query)
    return match.group(0) if match else None

def read_weather_data():
    """Read weather data from weather_api.txt."""
    weather_data = {}
    with open("weather_api.txt", "r") as file:
        for line in file:
            postal_code, city, temperature, condition = line.strip().split(",")
            weather_data[postal_code] = {
                "city": city,
                "temperature": int(temperature),
                "condition": condition
            }
    return weather_data

def fetch_calendar_events():
    """
    Simulate fetching calendar events from the owner's digital calendar.
    """
    return [
        {"event": "Meeting with client", "time": "10:00 AM", "location": "Melbourne Office"},
        {"event": "Lunch with team", "time": "1:00 PM", "location": "Melbourne Central"},
    ]

def get_lat_lon_from_location(location):
    """
    Get latitude and longitude from a location using Nominatim (OpenStreetMap).
    :param location: A string representing the location (e.g., "Melbourne, Australia").
    :return: A dictionary with latitude and longitude, or None if not found.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }
        response = requests.get(url, params=params)
        if response.status_code == 200 and response.json():
            result = response.json()[0]
            return {"lat": float(result["lat"]), "lon": float(result["lon"])}
        else:
            print(f"Location not found: {location}")
            return None
    except Exception as e:
        print(f"Error fetching latitude and longitude: {e}")
        return None


def fetch_charging_stations(location_name, battery_level):
    """
    Fetch real-time EV charging stations using Open Charge Map API.
    :param location_name: A string representing the location (e.g., "Melbourne, Australia").
    :param battery_level: The current battery level of the vehicle.
    :return: A list of charging stations or an error message.
    """
    if battery_level < 50:
        # Step 1: Get latitude and longitude from the location name
        coordinates = get_lat_lon_from_location(location_name)
        if not coordinates:
            return [{"error": "Could not fetch coordinates for the location."}]
        
        # Step 2: Fetch charging stations using Open Charge Map API
        api_key = "ddb1a969-6501-4547-9397-760d7fc3c4f1"  # Replace with your Open Charge Map API key
        url = "https://api.openchargemap.io/v3/poi/"
        params = {
            "latitude": coordinates["lat"],
            "longitude": coordinates["lon"],
            "maxresults": 5,
            "key": api_key
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                stations = response.json()
                return [{"station": station["AddressInfo"]["Title"], "distance": f"{station['AddressInfo'].get('Distance', 'N/A')} km"} for station in stations]
            else:
                print(f"Error fetching charging stations: {response.status_code} - {response.text}")
                return [{"error": "Failed to fetch charging stations."}]
        except Exception as e:
            print(f"Error fetching charging stations: {e}")
            return [{"error": "An error occurred while fetching charging stations."}]
    return [{"message": "Battery level is sufficient. No charging stations needed."}]

def prepare_vehicle_ambience(preferences, weather):
    """
    Simulate preparing the vehicle's ambience based on preferences and weather.
    """
    return {
        "climate": f"Set to {weather['temperature']}°C",
        "music": f"Playing {preferences.get('music', 'default playlist')}",
    }

def simulate_driver_fatigue(vehicle_status):
    """
    Simulate detecting driver fatigue based on vehicle status.
    """
    return vehicle_status.get("batteryLevel", 100) < 20

