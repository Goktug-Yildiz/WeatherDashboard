import tkinter as tk

def create_weather_display(root, app):
    weather_frame = tk.Frame(
        root, 
        bg=app.card_color, 
        padx=25, 
        pady=25,
        relief=tk.FLAT
    )
    return weather_frame

def display_weather(app, weather_data):
    # Clear previous weather data
    for widget in app.weather_frame.winfo_children():
        widget.destroy()