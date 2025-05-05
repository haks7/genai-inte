import re

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
        {"event": "Meeting with client", "time": "10:00 AM", "location": "Downtown Office"},
        {"event": "Lunch with team", "time": "1:00 PM", "location": "Café Central"},
    ]

def fetch_charging_stations(location, battery_level):
    """
    Simulate fetching charging stations based on location and battery level.
    """
    if battery_level < 50:
        return [{"station": "Station A", "distance": "5 km"}, {"station": "Station B", "distance": "10 km"}]
    return []

def suggest_stopovers(calendar_events, preferences):
    """
    Simulate suggesting stopovers based on calendar events and preferences.
    """
    return [{"type": "Restaurant", "name": "Vegan Delight", "distance": "2 km"}]

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