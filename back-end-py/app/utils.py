import re

def adjust_car_seat_heating(temperature):
    """Adjust the car seat heating system based on temperature."""
    if temperature < 10:
        return "Heating ON"
    elif 10 <= temperature <= 25:
        return "Heating OFF"
    else:
        return "Cooling ON"

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