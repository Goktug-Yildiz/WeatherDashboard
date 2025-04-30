import tkinter as tk
from app.api.weather_api import WeatherAPI
from app.api.wind_visualizer import WindVisualizer
from ui.main_window import setup_main_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ui.components.forecast import create_forecast_display  # Import the forecast component

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.api = WeatherAPI()
        self.wind_visualizer = WindVisualizer()
        self.historical_data = {}
        self.canvas_widget = None
        
        # Initialize UI
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
        location = self.location_entry.get().strip()
        if not location:
            self.status_label.config(text="Please enter a location")
            return
        
        self.status_label.config(text="Fetching weather data...", fg=self.text_color)
        self.root.update()
        
        try:
            # Get all weather data
            current_weather = self.api.get_current_weather(location)
            self.historical_data = self.api.get_historical_data(location)
            forecast_data = self.api.get_forecast(location)  # New forecast data
            
            if current_weather:
                if self.historical_data:
                    current_weather['one_hour_temp'] = self.historical_data['1_hour_ago']['temp_c']
                    current_weather['one_hour_time'] = self.historical_data['1_hour_ago']['time']
                
                # Pass forecast_data to display_weather
                self.display_weather(current_weather, forecast_data)
                self.plot_temperature_graph()
                self.status_label.config(text="")
                
        except Exception as e:
            self.weather_frame.pack_forget()
            self.status_label.config(text=f"Error: {str(e)}", fg="#dc3545")
            print(f"Error fetching weather: {e}")
    
    def plot_temperature_graph(self):
        if not self.historical_data or len(self.historical_data) < 2:
            return
        
        times = []
        temperatures = []
        
        for hour_key in sorted(self.historical_data.keys(), 
                             key=lambda x: int(x.split('_')[0])):
            entry = self.historical_data[hour_key]
            times.append(entry['time'])
            temperatures.append(entry['temp_c'])
        
        fig, ax = plt.subplots(figsize=(5, 2), dpi=70)
        ax.plot(times, temperatures, marker='o', linestyle='-', color='steelblue')
        ax.set_title("Past 12-Hour Temperatures")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temp (°C)")
        ax.grid(True)
        fig.tight_layout()
        
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
        
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.weather_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

    def set_and_search_location(self, location):
        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, location)
        self.get_weather()
    
    def display_weather(self, weather_data, forecast_data=None):
        """Updated to include forecast_data parameter"""
        # Clear previous widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        # Current weather display
        location_frame = tk.Frame(self.weather_frame, bg=self.card_color)
        location_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            location_frame,
            text=f"{weather_data['location']}, {weather_data['region']}",
            font=self.subtitle_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack(side="left")
        
        tk.Label(
            self.weather_frame,
            text=f"{weather_data['temperature']}°C",
            font=self.temp_font,
            bg=self.card_color,
            fg=self.primary_color
        ).pack(pady=10)
        
        tk.Label(
            self.weather_frame,
            text=weather_data['condition'],
            font=self.subtitle_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack()
        
        # Current conditions frame
        details_frame = tk.Frame(self.weather_frame, bg=self.card_color)
        details_frame.pack(pady=15)
        
        tk.Label(
            details_frame,
            text=f"Humidity: {weather_data['humidity']}%",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=10)
        
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
        
        # Historical temperature (1 hour ago)
        if 'one_hour_temp' in weather_data:
            tk.Label(
                self.weather_frame,
                text=f"1 hour ago: {weather_data['one_hour_temp']}°C at {weather_data['one_hour_time']}",
                font=self.small_font,
                bg=self.card_color,
                fg=self.secondary_color
            ).pack(pady=5)
        
        # Add forecast display if data exists
        if forecast_data:
            forecast_frame = create_forecast_display(self.weather_frame, self, forecast_data)
            forecast_frame.pack(fill="x", pady=15)
        
        # Make sure frame is visible
        self.weather_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.root.update_idletasks()