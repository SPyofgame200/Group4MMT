import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk

COLOR_BLUE_GRAY = "#1E3A4C"
COLOR_BRIGHT_CYAN = "#008080"
COLOR_HOVER = "#0099cc"  # Color for hover effect

def create_rounded_button_style():
    style = ttk.Style()
    style.configure("Rounded.TButton",
                    borderwidth=0,
                    relief="flat",
                    foreground='#9F2B68',
                    font=("Arial", 20, "bold"),
                    background="transparent")  # Set the background to transparent
    style.map("Rounded.TButton",
              background=[("active", "transparent"),
                          ("pressed", "transparent"),
                          ("-disabled", "transparent")])
    return style

def get_absolute_path(file_name):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, "pic", file_name) 

class TransparentButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        ttk.Button.__init__(self, master, style="Rounded.TButton", **kwargs)
        self.image = None

    def set_image(self, image):
        self.image = image
        self.configure(image=image, compound="center")

class HomePageUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure_ui(parent)
        self.add_background_image()
        self.add_buttons()
        self.add_disconnect_section()

    def configure_ui(self, parent):
        self.configure(
            bg=COLOR_BRIGHT_CYAN,
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")

    def add_background_image(self):
        original_image = Image.open(get_absolute_path("bg1.png"))
        ui_width = 1000
        ui_height = 600
        resized_image = original_image.resize((ui_width, ui_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label = tk.Label(self, image=self.background_image, bg='black')
        self.background_label.pack(fill='both', expand=True)

    def create_button(self, x, y, text, command):
        button = TransparentButton(
            self,
            text=text,
            command=command
        )
        button.place(
            x=x,
            y=y,
            width=150,
            height=50
        )
        return button

    def add_buttons(self):
        self.live_screen_button = self.create_button(127, 120, "Capture Screen", lambda: print("Live Screen clicked"))
        self.key_logger_button = self.create_button(127, 218, "Key Logger", lambda: print("Key Logger clicked"))
        self.app_process_button = self.create_button(127, 316, "App Process", lambda: print("App Process clicked"))
        self.shutdown_button = self.create_button(127, 414, "Shut Down", lambda: print("Shut Down clicked"))

    def add_disconnect_section(self):
        original_image = Image.open(get_absolute_path("bt3.png"))
        resized_image = original_image.resize((90, 90), Image.ANTIALIAS)
        disconnect_image = ImageTk.PhotoImage(resized_image)
        self.disconnect_button = TransparentButton(
            self,
            image=disconnect_image,
            command=lambda: print("Disconnect clicked")
        )
        self.disconnect_button.place(
            x=465,
            y=260,
        )
        self.disconnect_button.set_image(disconnect_image)