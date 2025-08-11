import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'http://api.weatherapi.com/v1/current.json?q={city}&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("data: ", data)
        weather = {
            'City': city,
            'Temperature in celsius': data['current']['temp_c'],
            'Humidity percentage': data['current']['humidity'],
            'Wind Speed in kph': data['current']['wind_kph']
        }
        return weather
    else:
        print(f"[!] Error: {response.status_code} - {response.json().get('message')}")
        return None

# Example usage
# api_key = ""  # Replace with your actual API key
# city = "Mumbai"
# weather_data = get_weather(city, api_key)

# if weather_data:
#     for key, value in weather_data.items():
#         print(f"{key}: {value}")
