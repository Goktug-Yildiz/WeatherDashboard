import tkinter as tk
import sys
from ui.components.header import create_header
from ui.components.input_frame import create_input_frame

def setup_main_window(root, app):
    root.title("Weather Forecast")
    root.geometry("600x850")
    root.resizable(True, True)
    
    # Create header frame for title and quit button
    header_frame = tk.Frame(
        root,
        bg=app.highlight_color,
        padx=25,
        pady=20,
        height=80
    )
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Application title (left side)
    title_label = tk.Label(
        header_frame,
        text="Weather Forecast",
        font=app.title_font,
        bg=app.highlight_color,
        fg=app.text_color
    )
    title_label.pack(side="left")

    # Quit button (right side) - now with full exit functionality
    quit_button = tk.Button(
        header_frame,
        text="Quit",
        command=lambda: [root.destroy(), sys.exit()],  # Destroy window and exit process
        bg="#dc3545",
        fg="white",
        font=app.subtitle_font,
        padx=15,
        pady=5,
        bd=0,
        relief=tk.FLAT,
        activebackground="#c82333",
        cursor="hand2"
    )
    quit_button.pack(side="right")

    # Create the rest of the UI components
    create_input_frame(root, app)
    
    return root