import tkinter as tk
from datetime import datetime
from app.api.weather_api import WeatherAPI
from app.api.wind_visualizer import WindVisualizer
from ui.main_window import setup_main_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from app.database.db_handler import DatabaseHandler

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.api = WeatherAPI()
        self.wind_visualizer = WindVisualizer()
        self.historical_data = {}
        self.canvas_widget = None
        self.db = DatabaseHandler()
        self.current_figure = None
        
        # Initialize UI
        self.setup_ui()
        self.create_weather_frame()
    
    def setup_ui(self):
        self.setup_styles()
        setup_main_window(self.root, self)
    
    def create_weather_frame(self):
        self.weather_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
            padx=10,
            pady=10
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
        self.title_font = ("Segoe UI", 18, "bold")
        self.subtitle_font = ("Segoe UI", 12)
        self.temp_font = ("Segoe UI", 36, "bold")  # Reduced from 42
        self.normal_font = ("Segoe UI", 10)
        self.small_font = ("Segoe UI", 8)
        
        self.root.configure(bg=self.bg_color)
    
    def get_weather(self):
        location = self.location_entry.get().strip()
        if not location:
            self.status_label.config(text="Please enter a location")
            return
        
        self.status_label.config(text="Fetching weather data...", fg=self.text_color)
        self.root.update()
        
        try:
            current_weather = self.api.get_current_weather(location)
            self.historical_data = self.api.get_historical_data(location)
            forecast_data = self.api.get_forecast(location)
            
            if current_weather:
                location_data ={
                    'city': current_weather['location'],
                    'region': current_weather['region'],
                    'country': current_weather['country']
                }
                weather_data = {
                    'temp': current_weather['temperature'],
                    'feels_like': current_weather['feels_like'],
                    'condition': current_weather['condition'],
                    'humidity': current_weather['humidity'],
                    'wind_speed': current_weather['wind_speed'],
                    'wind_degree': current_weather['wind_degree'],
                    'wind_dir': current_weather['wind_dir'],
                    'last_updated': current_weather['last_updated']
                }
                self.db.save_current_weather(location_data, weather_data)
                if self.historical_data:
                    current_weather['one_hour_temp'] = self.historical_data['1_hour_ago']['temp_c']
                    current_weather['one_hour_time'] = self.historical_data['1_hour_ago']['time']
                
                self.display_weather(current_weather, forecast_data)
                self.status_label.config(text="")
                
        except Exception as e:
            if hasattr(self, 'canvas_widget') and self.canvas_widget is not None:
                self.canvas_widget.get_tk_widget().destroy()
                plt.close(self.current_figure)
            
            self.weather_frame.pack_forget()
            self.status_label.config(text=f"Error: {str(e)}", fg="#dc3545")
            print(f"Error fetching weather: {e}")
    
    def display_weather(self, weather_data, forecast_data=None):
        # Clear previous widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        # Main dashboard container
        dashboard_frame = tk.Frame(self.weather_frame, bg=self.bg_color)
        dashboard_frame.pack(fill="both", expand=True)

        # Left column - Current weather
        left_column = tk.Frame(dashboard_frame, bg=self.bg_color)
        left_column.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Current weather card
        current_card = tk.Frame(left_column, bg=self.card_color, padx=15, pady=15, 
                               relief=tk.RIDGE, borderwidth=1)
        current_card.pack(fill="both", expand=True)

        # Location and time
        tk.Label(
            current_card,
            text=f"{weather_data['location']}, {weather_data['region']}",
            font=self.subtitle_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor="w")

        tk.Label(
            current_card,
            text=f"Updated: {weather_data['last_updated']}",
            font=self.small_font,
            bg=self.card_color,
            fg=self.secondary_color
        ).pack(anchor="w", pady=(0, 10))

        # Temperature and condition
        tk.Label(
            current_card,
            text=f"{weather_data['temperature']}°C",
            font=self.temp_font,
            bg=self.card_color,
            fg=self.primary_color
        ).pack()

        tk.Label(
            current_card,
            text=weather_data['condition'],
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).pack(pady=(0, 15))

        # Weather stats grid
        stats_frame = tk.Frame(current_card, bg=self.card_color)
        stats_frame.pack()

        tk.Label(
            stats_frame,
            text=f"Feels like: {weather_data['feels_like']}°C",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        tk.Label(
            stats_frame,
            text=f"Humidity: {weather_data['humidity']}%",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        tk.Label(
            stats_frame,
            text=f"Wind: {weather_data['wind_speed']} km/h",
            font=self.normal_font,
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Wind direction visualization
        wind_frame = tk.Frame(current_card, bg=self.card_color)
        wind_frame.pack(pady=10)

        wind_canvas = tk.Canvas(
            wind_frame,
            width=120,
            height=120,
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

        # Right column - Graph and forecast
        right_column = tk.Frame(dashboard_frame, bg=self.bg_color)
        right_column.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Temperature graph card
        graph_card = tk.Frame(right_column, bg=self.card_color, padx=10, pady=10,
                            relief=tk.RIDGE, borderwidth=1)
        graph_card.pack(fill="x", pady=(0, 10))

        if 'one_hour_temp' in weather_data:
            tk.Label(
                graph_card,
                text=f"1 hour ago: {weather_data['one_hour_temp']}°C at {weather_data['one_hour_time']}",
                font=self.small_font,
                bg=self.card_color,
                fg=self.secondary_color
            ).pack(anchor="w", pady=(0, 5))

        # Plot the temperature graph
        self.plot_temperature_graph(graph_card)

        # Forecast card
        if forecast_data:
            forecast_card = tk.Frame(right_column, bg=self.card_color, padx=10, pady=10,
                                   relief=tk.RIDGE, borderwidth=1)
            forecast_card.pack(fill="both", expand=True)

            tk.Label(
                forecast_card,
                text="3-Day Forecast",
                font=self.subtitle_font,
                bg=self.card_color,
                fg=self.primary_color
            ).pack(anchor="w", pady=(0, 10))

            # Forecast days container
            days_frame = tk.Frame(forecast_card, bg=self.card_color)
            days_frame.pack(fill="x")

            for i, day in enumerate(forecast_data['forecast']['forecastday'][:5]):
                day_card = tk.Frame(
                    days_frame,
                    bg=self.card_color,
                    padx=10,
                    pady=10,
                    relief=tk.GROOVE,
                    borderwidth=1
                )
                day_card.grid(row=0, column=i, padx=5, sticky="nsew")

                # Day name
                day_name = datetime.strptime(day['date'], "%Y-%m-%d").strftime("%a")
                tk.Label(
                    day_card,
                    text=day_name,
                    font=("Segoe UI", 10, "bold"),
                    bg=self.card_color,
                    fg=self.primary_color
                ).pack()

                # Weather emoji
                condition_emoji = self._get_condition_emoji(day['day']['condition']['text'])
                tk.Label(
                    day_card,
                    text=condition_emoji,
                    font=("Segoe UI", 20),
                    bg=self.card_color
                ).pack()

                # Temperatures
                tk.Label(
                    day_card,
                    text=f"{day['day']['mintemp_c']:.0f}° / {day['day']['maxtemp_c']:.0f}°",
                    font=self.normal_font,
                    bg=self.card_color,
                    fg=self.text_color
                ).pack()

                # Condition text
                tk.Label(
                    day_card,
                    text=day['day']['condition']['text'],
                    font=self.small_font,
                    bg=self.card_color,
                    fg=self.secondary_color,
                    wraplength=100
                ).pack()

        # Configure grid weights
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.columnconfigure(1, weight=1)
        dashboard_frame.rowconfigure(0, weight=1)

        self.weather_frame.pack(fill="both", expand=True)
        self.root.update_idletasks()

    def _get_condition_emoji(self, condition_text):
        """Helper to get emoji for weather condition"""
        condition = condition_text.lower()
        if "sun" in condition or "clear" in condition:
            return "☀️"
        elif "rain" in condition:
            return "🌧️"
        elif "cloud" in condition:
            return "☁️"
        elif "snow" in condition:
            return "❄️"
        elif "storm" in condition:
            return "⛈️"
        else:
            return "🌈"

    def plot_temperature_graph(self, parent_frame):
        if not self.historical_data or len(self.historical_data) < 2:
            # Show placeholder if no data
            tk.Label(
                parent_frame,
                text="Temperature data not available",
                bg=self.card_color,
                fg=self.secondary_color
            ).pack()
            return
        
        # Clear previous graph if exists
        if self.canvas_widget is not None:
            self.canvas_widget.get_tk_widget().destroy()
            plt.close(self.current_figure)
        
        # Prepare data
        times = []
        temperatures = []
        
        for hour_key in sorted(self.historical_data.keys(), 
                             key=lambda x: int(x.split('_')[0])):
            entry = self.historical_data[hour_key]
            times.append(entry['time'])
            temperatures.append(entry['temp_c'])
        
        # Create figure with constrained layout
        self.current_figure = Figure(figsize=(5, 2), dpi=80, tight_layout=True)
        ax = self.current_figure.add_subplot(111)
        
        # Plot data with improved styling
        ax.plot(times, temperatures, 
               marker='o', 
               markersize=4,
               linestyle='-', 
               linewidth=1.5,
               color='#3498db',
               markerfacecolor='#2980b9',
               markeredgecolor='white')
        
        # Style the plot
        ax.set_facecolor('#f8f9fa')
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.set_xlabel("Time", fontsize=8)
        ax.set_ylabel("°C", fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=7)
        
        # Create canvas widget
        self.canvas_widget = FigureCanvasTkAgg(self.current_figure, master=parent_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="x", expand=True)

    def set_and_search_location(self, location):
        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, location)
        self.get_weather()