import requests
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.key = os.getenv("key") or "88433e09e4c94c69a45174928252403" 
        self.base_url = "http://api.weatherapi.com/v1"
    
    def get_current_weather(self, location):
        try:
            params = {
                'key': self.key,
                'q': location,
                'aqi': "no"
            }
            response = requests.get(f"{self.base_url}/current.json", params=params)
            response.raise_for_status()
            weather_data = response.json()
            
            return {
                'location': weather_data['location']['name'],
                'region': weather_data['location']['region'],
                'country': weather_data['location']['country'],
                'temperature': weather_data['current']['temp_c'],
                'feels_like': weather_data['current']['feelslike_c'],
                'condition': weather_data['current']['condition']['text'],
                'humidity': weather_data['current']['humidity'],
                'wind_speed': weather_data['current']['wind_kph'],
                'wind_dir': weather_data['current']['wind_dir'],
                'wind_degree': weather_data['current']['wind_degree'],
                'last_updated': weather_data['current']['last_updated']
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {e}")
    
    def get_historical_data(self, location):
        try:
            end_time = datetime.now()
            historical_data = {}
            
            for hours_ago in range(1, 13):
                target_time = end_time - timedelta(hours=hours_ago)
                
                params = {
                    'key': self.key,
                    'q': location,
                    'dt': target_time.strftime("%Y-%m-%d"),
                    'hour': target_time.hour
                }
                response = requests.get(f"{self.base_url}/history.json", params=params)
                response.raise_for_status()
                data = response.json()
                
                hour_data = data['forecast']['forecastday'][0]['hour'][0]
                historical_data[f'{hours_ago}_hour_ago'] = {
                    'temp_c': hour_data['temp_c'],
                    'time': target_time.strftime("%H:%M"),
                    'wind_kph': hour_data['wind_kph'],
                    'wind_dir': hour_data['wind_dir'],
                    'condition': hour_data['condition']['text'],
                    'humidity': hour_data['humidity']
                }
                
                if hours_ago < 12:
                    time.sleep(1)
            
            return historical_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching historical data: {e}")