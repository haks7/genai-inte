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