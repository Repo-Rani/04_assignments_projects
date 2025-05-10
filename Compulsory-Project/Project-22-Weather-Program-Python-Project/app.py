import requests
from dotenv import load_dotenv
import os

load_dotenv(".env.local")

API_KEY = os.getenv("API_KEY")

def get_weather(city_name):
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] != 200:
            print(f"❌ Error: {data['message']}")
        else:
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            print(f"\n📍 Weather in {city_name.title()}:")
            print(f"🌡 Temperature: {temp}°C (Feels like {feels_like}°C)")
            print(f"🌤 Condition: {weather}")
            print(f"💧 Humidity: {humidity}%")
            print(f"💨 Wind Speed: {wind_speed} m/s\n")

    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":
    city = input("Enter a city name: ")
    get_weather(city)