import requests
import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")

# Cache to store weather data
weather_cache = {}

def fetch_weather_data(city_or_postal_code):
    """Fetch weather data from OpenWeatherMap API and cache it."""
    try:
        # Check if the data is already in the cache
        if city_or_postal_code in weather_cache:
            print(f"Returning cached weather data for {city_or_postal_code}")
            return weather_cache[city_or_postal_code]

        if not WEATHER_API_KEY:
            raise ValueError("Weather API key is missing. Please set it in the environment.")

        if not WEATHER_API_URL:
            raise ValueError("Weather API URL is missing. Please set it in the environment.")

        # Construct the full URL with query parameters
        params = {
            "q": city_or_postal_code,  # City name or postal code
            "appid": WEATHER_API_KEY,  # API key
            "units": "metric",  # Get temperature in Celsius
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        city_weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
        }

        # Save the data in the cache
        weather_cache[city_or_postal_code] = city_weather
        print(f"Weather data cached for {city_or_postal_code}: {city_weather}")

        return city_weather
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Debugging log
        raise
    except Exception as e:
        print(f"Error fetching weather data: {e}")  # Debugging log
        raise