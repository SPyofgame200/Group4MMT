import os
import sys
import tkinter as tk
from tkinter import Button, Frame, Label, Text
from PIL import ImageTk, Image

BUFFER_SIZE = 1024 * 4


def get_absolute_path(file_name):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'pic\\' + file_name)


def toggle_button(client, button, message):
    client.sendall(bytes(message, "utf8"))
    button.configure(text=message if button['text'] != message else message)


def send_message_and_print(client, textbox, message):
    client.sendall(bytes(message, "utf8"))
    data = client.recv(BUFFER_SIZE).decode("utf8")[1:]
    textbox.config(state="normal")
    textbox.insert(tk.END, data)
    textbox.config(state="disable")


def clear_textbox(textbox):
    textbox.config(state="normal")
    textbox.delete("1.0", "end")
    textbox.config(state="disable")


class KeyloggerUI(Frame):
    def __init__(self, parent, client):
        super().__init__(parent, bg="#008080", height=600, width=1000, bd=0, highlightthickness=0, relief="ridge")
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        # Initialize UI elements
        self.initialize_ui_elements(client)

    def initialize_ui_elements(self, client):
        self.initialize_background_image()
        self.initialize_textbox()
        self.initialize_buttons(client)
        self.initialize_footer_image()

    def initialize_background_image(self):
        background_image = ImageTk.PhotoImage(Image.open(get_absolute_path("bg9.jpg")))
        background_label = Label(self, image=background_image, bg='#40E0D0')
        background_label.place(x=0, y=0)

    def initialize_textbox(self):
        self.textbox = Text(self, height=200, width=500, state="disable", wrap="char", bd=0, bg='white',
                            highlightthickness=0)
        self.textbox.place(x=220, y=100, width=600, height=360)

    def initialize_buttons(self, client):
        self.button_hook = self.create_button('HOOK', lambda: toggle_button(client, self.button_hook, 'HOOK'), 850, 150)
        self.button_lock = self.create_button('LOCK', lambda: toggle_button(client, self.button_lock, 'LOCK'), 850, 300)
        self.button_print = self.create_button('PRINT', lambda: send_message_and_print(client, self.textbox, 'PRINT'),
                                               30, 150)
        self.button_delete = self.create_button('DELETE', lambda: clear_textbox(self.textbox), 30, 300)
        self.button_back = self.create_button('BACK', lambda: None, 740, 520)

    def initialize_footer_image(self):
        # Load the image
        footer_image = Image.open(get_absolute_path("bg7.jpg"))

        # Calculate the scaling factor to fit the specified dimensions
        width, height = 135, 53
        aspect_ratio = width / float(footer_image.width)
        new_height = int(footer_image.height * aspect_ratio)

        # Resize the image while maintaining its aspect ratio
        footer_image = footer_image.resize((width, new_height), Image.ANTIALIAS)

        # Convert the image to PhotoImage format
        footer_image = ImageTk.PhotoImage(footer_image)

        footer_label = Label(self, image=footer_image)
        footer_label.image = footer_image  # Store a reference to prevent image from being garbage collected
        footer_label.place(x=440, y=500)

    def create_button(self, text, command, x, y):
        # Create a custom button style with hover effect
        button_style = {
            'text': text, 'width': 20, 'height': 5, 'fg': '#d4d4d4', 'bg': '#4d4d4d', 'borderwidth': 0,
            'highlightthickness': 0, 'font': 'Helvetica 15 bold', 'command': command, 'relief': "raised"
        }

        # Create a rounded button with a highlight effect
        button = FancyButton(self, **button_style)
        button.place(x=x, y=y, width=135, height=53)
        return button


class FancyButton(Button):
    def __init__(self, master=None, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.default_bg = kwargs['bg']
        self.configure(
            relief=tk.RAISED,  # Makes the button look raised
            highlightcolor="lightgray",  # Color when the button is clicked
            highlightbackground="black",  # Background color of the button border
            padx=5,  # Padding on the left and right
            pady=5,  # Padding on the top and bottom
            borderwidth=2  # Border width
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self['bg'] = '#9F2B68'

    def on_leave(self, event):
        self['bg'] = self.default_bg


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerUI(root, None)  # Replace None with your client object
    root.mainloop()
