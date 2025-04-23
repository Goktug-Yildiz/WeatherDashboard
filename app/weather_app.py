import tkinter as tk
from app.api.weather_api import WeatherAPI
from app.api.wind_visualizer import WindVisualizer
from ui.main_window import setup_main_window

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.api = WeatherAPI()
        self.wind_visualizer = WindVisualizer()
        self.historical_data = {}
        
        self.setup_ui()
        
        self.create_weather_frame()
    
    def setup_ui(self):
        self.setup_styles()
        setup_main_window(self.root, self)
    
    def create_weather_frame(self):
        self.weather_frame = tk.Frame(
            self.root,
            bg=self.card_color,
            padx=20,
            pady=20,
            relief=tk.FLAT
        )
    
    def setup_styles(self):
        """Configure color and font styles"""
        # Color palette
        self.bg_color = "#f5f5f5"
        self.primary_color = "#495057"
        self.secondary_color = "#6c757d"
        self.accent_color = "#adb5bd"
        self.text_color = "#212529"
        self.card_color = "#ffffff"
        self.wind_color = "#6c757d"
        self.highlight_color = "#dee2e6"
        
        # Font styles
        self.title_font = ("Segoe UI", 22, "bold")
        self.subtitle_font = ("Segoe UI", 13)
        self.temp_font = ("Segoe UI", 42, "bold")
        self.normal_font = ("Segoe UI", 11)
        self.small_font = ("Segoe UI", 9)
        
        self.root.configure(bg=self.bg_color)
    
    def get_weather(self):
        """Fetch and display weather data"""
        location = self.location_entry.get().strip()
        if not location:
            self.status_label.config(text="Please enter a location")
            return
        
        self.status_label.config(text="Fetching weather data...", fg=self.text_color)
        self.root.update()
        
        try:
            current_weather = self.api.get_current_weather(location)
            one_hour_data = self.api.get_historical_data(location)
            
            if current_weather:
                if one_hour_data:
                    current_weather['one_hour_temp'] = one_hour_data['1_hour_ago']['temp_c']
                    current_weather['one_hour_time'] = one_hour_data['1_hour_ago']['time']
                self.display_weather(current_weather)
                self.status_label.config(text="")
        except Exception as e:
            self.weather_frame.pack_forget()
            self.status_label.config(text=f"Error: {str(e)}", fg="#dc3545")
            print(f"Error fetching weather: {e}")
    
    def display_weather(self, weather_data):
        """Display weather information in the UI"""
        # Clear previous widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        # Location information
        location_frame = tk.Frame(self.weather_frame, bg=self.card_color)
        location_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            location_frame,
            text=f"{weather_data['location']}, {weather_data['region']}",
            font=self.subtitle_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack(side="left")
        
        # Temperature display
        tk.Label(
            self.weather_frame,
            text=f"{weather_data['temperature']}°C",
            font=self.temp_font,
            bg=self.card_color,
            fg=self.primary_color
        ).pack(pady=10)
        
        # Weather condition
        tk.Label(
            self.weather_frame,
            text=weather_data['condition'],
            font=self.subtitle_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack()
        
        # Additional details frame
        details_frame = tk.Frame(self.weather_frame, bg=self.card_color)
        details_frame.pack(pady=15)
        
        # Humidity
        tk.Label(
            details_frame,
            text=f"Humidity: {weather_data['humidity']}%",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=10)
        
        # Wind speed
        tk.Label(
            details_frame,
            text=f"Wind: {weather_data['wind_speed']} km/h",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=1, padx=10)
        
        # Wind direction visualization
        wind_frame = tk.Frame(self.weather_frame, bg=self.card_color)
        wind_frame.pack(pady=10)
        
        wind_canvas = tk.Canvas(
            wind_frame,
            width=150,
            height=180,
            bg=self.card_color,
            highlightthickness=0
        )
        wind_canvas.pack()
        
        self.wind_visualizer.draw_wind_direction(
            wind_canvas,
            weather_data['wind_degree'],
            weather_data['wind_speed'],
            {'wind': self.wind_color}
        )
        
        # Historical data if available
        if 'one_hour_temp' in weather_data:
            tk.Label(
                self.weather_frame,
                text=f"1 hour ago: {weather_data['one_hour_temp']}°C at {weather_data['one_hour_time']}",
                font=self.small_font,
                bg=self.card_color,
                fg=self.secondary_color
            ).pack(pady=5)
        
        # Make sure frame is visible
        self.weather_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.root.update_idletasks()