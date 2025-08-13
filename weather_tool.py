import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Weather API to fetch weather data
def get_weather(city: str):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'http://api.weatherapi.com/v1/current.json?q={city}&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print("data: ", data)

        return f"Temrature is {data['current']['temp_c']} celcius, Humidity is {data['current']['humidity']}%, Wind speed is {data['current']['wind_kph']} kph and overall condition is {data['current']['condition']['text']}"
    else:
        print(f"[!] Error: {response.status_code} - {response.json().get('message')}")
        return "Weather information is not available of this city, please choose a different city."

# Example usage
# api_key = ""  # Replace with your actual API key
# city = "Mumbai"
# weather_data = get_weather(city, api_key)

# if weather_data:
#     for key, value in weather_data.items():
#         print(f"{key}: {value}")
