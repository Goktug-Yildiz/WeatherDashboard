import tkinter as tk

def create_forecast_display(parent, app, forecast_data):
    frame = tk.Frame(parent, bg=app.card_color, padx=10, pady=10)
    
    tk.Label(
        frame,
        text="3-Day Forecast",
        font=app.subtitle_font,
        bg=app.card_color,
        fg=app.primary_color
    ).pack(anchor="w")
    
    for day in forecast_data['forecast']['forecastday']:
        day_frame = tk.Frame(frame, bg=app.card_color)
        day_frame.pack(fill="x", pady=5)
        
        date = tk.Label(
            day_frame,
            text=day['date'],
            font=app.normal_font,
            bg=app.card_color,
            fg=app.text_color,
            width=10
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
    
    return frame