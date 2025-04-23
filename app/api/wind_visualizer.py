import tkinter as tk
import math

class WindVisualizer:
    def draw_wind_direction(self, canvas, degree, speed, colors):
        """Draw a complete wind direction compass with arrow and labels"""
        canvas.delete("all")
        
        center_x, center_y = 75, 75
        radius = 60
        
        # Draw compass circle
        canvas.create_oval(
            center_x - radius, 
            center_y - radius,
            center_x + radius, 
            center_y + radius,
            outline=colors['wind'],
            width=2
        )
        
        # Draw axis lines (N, E, S, W)
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x1 = center_x + (radius - 15) * math.cos(rad)
            y1 = center_y - (radius - 15) * math.sin(rad)
            x2 = center_x + radius * math.cos(rad)
            y2 = center_y - radius * math.sin(rad)
            canvas.create_line(x1, y1, x2, y2, fill=colors['wind'], width=2)
        
        # Draw cardinal directions
        for angle, direction in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
            rad = math.radians(angle)
            dir_x = center_x + (radius - 25) * math.cos(rad)
            dir_y = center_y - (radius - 25) * math.sin(rad)
            canvas.create_text(
                dir_x, dir_y,
                text=direction,
                font=("Arial", 10, "bold"),
                fill=colors['wind']
            )
        
        # Draw intercardinal directions (NE, SE, SW, NW)
        for angle, direction in [(45, "NE"), (135, "SE"), (225, "SW"), (315, "NW")]:
            rad = math.radians(angle)
            dir_x = center_x + (radius - 20) * math.cos(rad)
            dir_y = center_y - (radius - 20) * math.sin(rad)
            canvas.create_text(
                dir_x, dir_y,
                text=direction,
                font=("Arial", 8),
                fill=colors['wind']
            )
        
        # Draw wind direction arrow
        rad = math.radians(degree)
        arrow_length = radius - 15
        
        end_x = center_x + arrow_length * math.cos(rad)
        end_y = center_y - arrow_length * math.sin(rad)
        
        canvas.create_line(
            center_x, center_y, end_x, end_y, 
            fill="#3498db", 
            width=3, 
            arrow=tk.LAST,
            arrowshape=(10, 12, 5)
        )
        # Add wind speed and direction text
        canvas.create_text(
            center_x, center_y + radius + 20,
            text=f"{speed} km/h {self.get_wind_direction_name(degree)}",
            font=("Arial", 9),
            fill=colors['wind']
        )
    
    def get_wind_direction_name(self, degree):
        """Convert wind degree to compass direction name"""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                     "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        index = round(degree / (360. / len(directions))) % len(directions)
        return directions[index]