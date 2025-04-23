import tkinter as tk

def create_header(root, app):
    header_frame = tk.Frame(
        root, 
        bg=app.highlight_color, 
        padx=25, 
        pady=20,
        height=80
    )
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame, 
        text="Weather Forecast", 
        font=app.title_font, 
        bg=app.highlight_color, 
        fg=app.text_color
    )
    title_label.pack(side="left")