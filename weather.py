import requests, os, dotenv
from pathlib import Path

dotenv.load_dotenv(Path(__file__).parent / ".env")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

LANGUAGE = "en"
UNITS = "metric"


def get_city():
    '''Gets the current city based on the public IP address.'''
    try:
        url = f"https://ipinfo.io/json?token={IPINFO_TOKEN}"
        response = requests.get(url, timeout=3)

        if response.status_code == 200:
            return response.json().get("city")

        return None

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout
    ):
        return None


def get_weather():
    '''Calls the OpenWeatherMap API to fetch current weather data.'''

    city_name = get_city()

    if not city_name:
        return None, None, None, None

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_name}"
        f"&appid={WEATHER_API_KEY}"
        f"&lang={LANGUAGE}"
        f"&units={UNITS}"
    )

    try:
        response = requests.get(url=url, timeout=3)

        if response.status_code == 200:
            data = response.json()

            weather = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]

            return weather, temp, feels_like, humidity

        else:
            print(f"An error occurred. Status code: {response.status_code}")
            print("Please check that the API keys are correct.")

            return None, None, None, None

    except requests.exceptions.ConnectionError as e:
        print(f"Network Connection Error: {e}")
        return None, None, None, None

    except requests.exceptions.Timeout as e:
        print(f"The server is too busy, or the network connection is poor: {e}")
        return None, None, None, None