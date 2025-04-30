import mysql.connector
from mysql.connector import Error

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='weather_app'
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def save_current_weather(self, location_data, weather_data):
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # Insert or get location
            cursor.execute("""
                INSERT INTO locations (city, region, country)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE location_id=LAST_INSERT_ID(location_id)
            """, (location_data['city'], location_data['region'], location_data['country']))
            
            location_id = cursor.lastrowid
            
            # Insert weather data
            cursor.execute("""
                INSERT INTO weather_data (
                    location_id, temperature, feels_like, condition_text,
                    humidity, wind_speed, wind_degree, wind_dir, last_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                location_id,
                weather_data['temp'],
                weather_data['feels_like'],
                weather_data['condition'],
                weather_data['humidity'],
                weather_data['wind_speed'],
                weather_data['wind_degree'],
                weather_data['wind_dir'],
                weather_data['last_updated']
            ))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error saving weather data: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def save_forecast(self, location_data, forecast_data):
        # Similar implementation for forecasts
        pass
    
    def get_historical_data(self, location, days=7):
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT location_id FROM locations 
                WHERE city = %s AND region = %s AND country = %s
            """, (location['city'], location['region'], location['country']))
            
            location_result = cursor.fetchone()
            if not location_result:
                return None
                
            cursor.execute("""
                SELECT * FROM weather_data
                WHERE location_id = %s
                ORDER BY last_updated DESC
                LIMIT %s
            """, (location_result['location_id'], days))
            
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching historical data: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()