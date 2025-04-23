import tkinter as tk
from ui.components.header import create_header
from ui.components.input_frame import create_input_frame

def setup_main_window(root, app):
    root.title("Weather Forecast")
    root.geometry("600x850")
    root.resizable(True, True)
    
    # Create all UI components
    create_header(root, app)
    create_input_frame(root, app)
    
    return root