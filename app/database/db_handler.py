import mysql.connector
from mysql.connector import Error

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.is_connected = False
        self.connect()
    
    def connect(self):
        """Attempt to connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='weather_app',
                autocommit=False
            )
            self.is_connected = True
            print("Successfully connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.is_connected = False
        return self.is_connected
    
    def ensure_connection(self):
        if not self.is_connected:
            return self.connect()
        
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=1)
            return True
        except Error:
            self.is_connected = False
            return self.connect()
    
    def save_current_weather(self, location_data, weather_data):
        if not self.ensure_connection():
            print("Database not available - skipping save")
            return False
            
        cursor = None
        try:
            cursor = self.connection.cursor() 
            cursor.execute("""
                INSERT INTO locations (city, region, country)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE location_id=LAST_INSERT_ID(location_id)
            """, (location_data['city'], location_data['region'], location_data['country']))
            
            location_id = cursor.lastrowid
            
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
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.is_connected = False
            print("Database connection closed")