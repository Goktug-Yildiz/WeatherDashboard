import tkinter as tk
from tkinter import ttk

def create_input_frame(root, app):
    input_frame = tk.Frame(
        root, 
        bg=app.bg_color, 
        padx=30, 
        pady=25
    )
    input_frame.pack(fill="x")
    
    # Location label
    location_label = tk.Label(
        input_frame, 
        text="Enter location:", 
        font=app.subtitle_font, 
        bg=app.bg_color,
        fg=app.text_color
    )
    location_label.grid(row=0, column=0, sticky="w", pady=(0, 8), columnspan=2)
    
    # Location entry
    app.location_entry = tk.Entry(
        input_frame, 
        font=app.normal_font, 
        width=28,
        bd=1,
        relief=tk.SOLID,
        highlightthickness=0,
        bg=app.card_color
    )
    app.location_entry.grid(row=1, column=0, sticky="we")
    app.location_entry.bind("<Return>", lambda event: app.get_weather())
    
    # Search button
    search_button = tk.Button(
        input_frame, 
        text="Search", 
        command=lambda: app.get_weather(),
        bg=app.primary_color, 
        fg="white",
        font=app.subtitle_font,
        padx=18,
        pady=6,
        bd=0,
        activebackground=app.secondary_color,
        activeforeground="white",
        cursor="hand2"
    )
    search_button.grid(row=1, column=1, padx=(10, 20))
    
    # Shortcut locations frame
    shortcuts_frame = tk.Frame(input_frame, bg=app.bg_color)
    shortcuts_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="w")
    
    # Shortcut buttons
    shortcut_locations = [
        ("Athens", "Athens"),
        ("Istanbul", "Istanbul"),
        ("London", "London"),
        ("Washington", "Washington,DC")
    ]
    
    for i, (btn_text, location) in enumerate(shortcut_locations):
        btn = tk.Button(
            shortcuts_frame,
            text=btn_text,
            command=lambda loc=location: app.set_and_search_location(loc),
            bg=app.accent_color,
            fg=app.text_color,
            font=app.small_font,
            padx=10,
            pady=3,
            bd=0,
            activebackground=app.highlight_color,
            cursor="hand2"
        )
        btn.grid(row=0, column=i, padx=(0, 10))
    
    # Status Label
    app.status_label = tk.Label(
        root, 
        text="", 
        font=app.small_font, 
        bg=app.bg_color,
        fg="#dc3545"
    )
    app.status_label.pack(pady=8)