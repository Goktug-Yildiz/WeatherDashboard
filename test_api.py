""" from app.api.weather_api import WeatherAPI

def test_weather_api():
    api = WeatherAPI()
    
    # Test current weather
    print("\nTesting current weather API:")
    try:
        current = api.get_current_weather("Ankara")
        print("Success! Current weather data:")
        print(f"Location: {current['location']}, Temp: {current['temperature']}°C")
    except Exception as e:
        print(f"Current weather failed: {str(e)}")
    
    # Test historical data
    print("\nTesting historical weather API:")
    try:
        historical = api.get_weather_historical("Ankara")
        print("Success! Historical data sample:")
        print(f"1 hour ago: {historical['1_hour_ago']['temp_c']}°C at {historical['1_hour_ago']['time']}")
    except Exception as e:
        print(f"Historical data failed: {str(e)}")

if __name__ == "__main__":
    test_weather_api() """