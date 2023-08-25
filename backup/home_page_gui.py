import tkinter as tk
from tkinter import  ttk
import pickle, struct
from tkinter import*
from PIL import Image, ImageTk
import os
import sys

COLOR_BLUE_GRAY = "#1E3A4C"
COLOR_BRIGHT_CYAN = "#008080"
COLOR_HOVER = "#0099cc"  # Color for hover effect

# Add this function to create a rounded button style
def create_rounded_button_style():
    style = ttk.Style()
    style.configure("Rounded.TButton",
                    borderwidth=0,
                    relief="flat",
                    foreground='#9F2B68',
                    background=COLOR_BLUE_GRAY,
                    font='Helvetica 20 bold',
                    padding=(10, 10))
    style.map("Rounded.TButton",
              background=[("active", COLOR_HOVER)])
    return style

def get_absolute_path(file_name):
    """ 
    Get absolute path to resource, works for dev and for PyInstaller 
    """
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") 

    return os.path.join(base_path, file_name) 

class HomePageUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure_ui(parent)
        self.add_background_image()
        self.add_buttons()
        self.add_disconnect_section()

    def configure_ui(self, parent):
        """
        Configure UI settings
        """
        self.configure(
            bg = COLOR_BRIGHT_CYAN,
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        
    def add_background_image(self):
        """
        Add background image to UI and resize it to fit the scale
        """
        # Load the original image
        original_image = Image.open(get_absolute_path("bg1.png"))

        # Get the dimensions of the UI (you can adjust this as needed)
        ui_width = 1000
        ui_height = 600

        # Resize the image to fit the UI
        resized_image = original_image.resize((ui_width, ui_height), Image.ANTIALIAS)

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Create a label with the resized image
        self.background_label = Label(self, image=self.background_image, bg='black')
        self.background_label.pack(fill='both', expand=True)

    def create_button(self, x, y, text, command):
        # Use ttk.Button with the custom "Rounded.TButton" style
        button = ttk.Button(
            self,
            text=text,
            style="Rounded.TButton",
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
        """
        Add buttons to UI
        """
        self.live_screen_button = self.create_button(127, 120, "Capture Screen", lambda: print("Live Screen clicked"))
        self.key_logger_button = self.create_button(127, 218, "Key Logger", lambda: print("Key Logger clicked"))
        self.app_process_button = self.create_button(127, 316, "App Process", lambda: print("App Process clicked"))
        self.shutdown_button = self.create_button(127, 414, "Shut Down", lambda: print("Shut Down clicked"))

    def add_disconnect_section(self):
        """
        Add disconnect section to UI
        """
        self.disconnect_image = ImageTk.PhotoImage(Image.open(get_absolute_path("bt3.jpg")))
        self.disconnect_button = Button(
            self,
            image=self.disconnect_image,
            bg='black',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Disconnect clicked"),
            relief="flat"
        )
        self.disconnect_button.place(
            x=470,
            y=260,
        )

if __name__ == "__main__":
    root = tk.Tk()
    style = create_rounded_button_style()
    app = HomePageUI(root)
    root.mainloop()