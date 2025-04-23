import tkinter as tk

def create_input_frame(root, app):
    input_frame = tk.Frame(
        root, 
        bg=app.bg_color, 
        padx=30, 
        pady=25
    )
    input_frame.pack(fill="x")
    
    location_label = tk.Label(
        input_frame, 
        text="Enter location:", 
        font=app.subtitle_font, 
        bg=app.bg_color,
        fg=app.text_color
    )
    location_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
    
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
    search_button.grid(row=1, column=1, padx=12)
    
    # Status Label
    app.status_label = tk.Label(
        root, 
        text="", 
        font=app.small_font, 
        bg=app.bg_color,
        fg="#dc3545"
    )
    app.status_label.pack(pady=8)