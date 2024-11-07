import requests
from datetime import datetime, timedelta

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather():
    api_key = "7a3cb00ba1ef503e8edd6fd052d6ddfb"  # Replace with your actual OpenWeatherMap API key
    city = "Haldwani"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        today = datetime.now().date()
        
        results = []
        # Filter forecasts for today and the next 6 days
        for forecast in data['list']:
            forecast_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if today <= forecast_time.date() <= today + timedelta(days=6):
                temp = kelvin_to_celsius(forecast['main']['temp'])
                description = forecast['weather'][0]['description']
                results.append(f"Date & Time: {forecast_time} | Temp: {temp:.2f}°C | Weather: {description}")

        return "\n".join(results)
    else:
        return "Could not retrieve weather data"