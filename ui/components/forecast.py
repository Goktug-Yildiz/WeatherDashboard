""" import tkinter as tk
from datetime import datetime

def create_forecast_display(parent, app, forecast_data):
    frame = tk.Frame(parent, bg=app.card_color, padx=15, pady=15)
    
    tk.Label(
        frame,
        text=f"{len(forecast_data['forecast']['forecastday'])}-Day Forecast",  # Dynamic count
        font=app.subtitle_font,
        bg=app.card_color,
        fg=app.primary_color
    ).pack(anchor="w")
    
    for day in forecast_data['forecast']['forecastday']:
        # Convert date to more readable format (e.g., "Mon, Jan 10")
        date_obj = datetime.strptime(day['date'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%a, %b %d")
        
        day_frame = tk.Frame(frame, bg=app.card_color)
        day_frame.pack(fill="x", pady=5)
        
        date = tk.Label(
            day_frame,
            text=formatted_date,
            font=app.normal_font,
            bg=app.card_color,
            fg=app.text_color,
            width=12
        )
        date.pack(side="left")
        
        tk.Label(
            day_frame,
            text=f"↑{day['day']['maxtemp_c']}° ↓{day['day']['mintemp_c']}°",
            font=app.normal_font,
            bg=app.card_color,
            fg=app.text_color,
            width=15
        ).pack(side="left")
        
        tk.Label(
            day_frame,
            text=day['day']['condition']['text'],
            font=app.normal_font,
            bg=app.card_color,
            fg=app.text_color,
            width=25
        ).pack(side="left")
    
    return frame """