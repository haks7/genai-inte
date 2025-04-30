import re
from azure.storage.blob import BlobServiceClient
import os

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
    postal_code = match.group(0) if match else None
    print(f"Extracted postal code: {postal_code}")  # Debugging log
    return postal_code

def read_weather_data_from_storage():
    """Read weather data from Azure Blob Storage."""
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    blob_name = "weather_api.txt"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        blob_data = blob_client.download_blob().readall().decode("utf-8")
        lines = blob_data.strip().split("\n")
        weather_data = {}
        for line in lines:
            postal_code, city, temperature, condition = line.split(",")
            weather_data[postal_code.strip()] = {
                "city": city.strip(),
                "temperature": float(temperature.strip()),
                "condition": condition.strip()
            }
        print(f"Loaded weather data: {weather_data}")  # Debugging log
        return weather_data
    except Exception as e:
        print(f"Error reading weather data from Azure Storage: {e}")
        return None