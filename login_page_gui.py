import tkinter as tk
from tkinter import font
from tkinter import Entry, Button, StringVar
from PIL import Image, ImageTk
import os
import sys

def get_resource_path(file_name):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    file_name = 'pic\\' + file_name
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, file_name)

class LogInPageUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.configure(
            bg="#008080",
            height=500,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        parent.geometry("800x500+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        self.left_frame = tk.Frame(self, height=500, width=400, bg='black')
        self.left_frame.place(x=0, y=0)
        self.right_frame = tk.Frame(self, height=500, width=400, bg='black')
        self.right_frame.place(x=400, y=0)

        # Use get_resource_path to get the full path to the image files
        left_image = ImageTk.PhotoImage(Image.open(get_resource_path("bg2.jpg")))
        self.left_image = ImageTk.PhotoImage(Image.open(get_resource_path("bg2.jpg")))
        self.left_image_label = tk.Label(self.left_frame, image=self.left_image, bg='black')
        self.left_image_label.image = self.left_image  # Keep a reference to the image

        self.left_image_label.place(x=0, y=0)

        heading = tk.Label(
            self.right_frame,
            text='Your IP Address (IPv4: x.x.x.x)',
            font='arial 15 bold',
            bg='black',
            fg='#9F2B68')
        heading.place(x=80, y=150)

        my_font = font.Font(family='Helvetica', size=20)
        self.input_ip_address = StringVar()
        self.input_ip_address.set("Enter Address")  # Set the default text
        self.ip_address_entry = EntryWithPlaceholder(
            self.right_frame,
            textvariable=self.input_ip_address,
            placeholder="Enter IP Address",
            bg="#B7C9E2",
            fg='grey',
            font=my_font
        )
        self.ip_address_entry.place(x=60, y=200, width=300.0, height=58.0)

        # Use get_resource_path to get the full path to the image files
        right_image = Image.open(get_resource_path("pbtt.png"))
        # Resize the image to fit within a 50x50 pixel button
        right_image = right_image.resize((50, 50), Image.LANCZOS)
        right_image = ImageTk.PhotoImage(right_image)

        self.submit_button = tk.Button(
            self.right_frame,
            image=right_image,
            bg='black',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.submit_button.image = right_image  # Keep a reference to the image

        self.submit_button.place(
            x=180,
            y=300,
            height=50,
            width=50,
        )
        self.ip_address_entry.bind("<Return>", self.submit_button_click)

    def submit_button_click(self, event):
        # Simulate a button click when Enter is pressed
        self.submit_button.invoke()

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.default_fg_color = self["fg"]
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.typing = False
        self.bind("<Key>", self.typing_started)  # Bind the Key event to track typing
        self.bind("<KeyRelease>", self.validate_input)  # Bind the KeyRelease event for input validation
        self.put_placeholder()
        
    def typing_started(self, event):
        self.typing = True
        self.config(fg='#701934')  # Set text color to orange after validation

    def put_placeholder(self):
        if not self.get() and not self.typing:
            self.set_placeholder()

    def set_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg='grey')  # Set text color to gray

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)  # Restore default text color

    def on_focus_out(self, event):
        if not self.get():
            self.set_placeholder()
        
    def validate_input(self, event):
        if self.typing == False:
            return 
        
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Shift_R', 'Shift_L'):
            return 
            
        # Check if Ctrl key is pressed along with a key
        ctrl_pressed = (event.state & 0x4) != 0  # 0x4 corresponds to the Control key

        if ctrl_pressed and event.keysym in ('a', 'c', 'x', 'v'):
            return  # Ctrl+A, Ctrl+C, Ctrl+X, Ctrl+V are allowed

        # Get the current content of the entry field
        current_value = self.get()
        
        # If the input is the placeholder or empty, allow it
        if current_value == self.placeholder or current_value == "":
            return

        # User is typing, remove the placeholder
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)  # Restore default text color

        # Remove dots at the beginning and limit to three dots
        
        current_value = current_value.lstrip('.')
        parts = current_value.split('.')
        if len(parts) >= 4:
            # Remove extra dots if there are more than three
            current_value = '.'.join(parts[:3]) + '.' + parts[3]

        # Remove any characters that are not numerals or dots
        clean_value = "".join(char for char in current_value if char.isdigit() or char == '.')

        # Truncate the input to 15 characters
        clean_value = clean_value[:15]

        # Split the input by dots and validate each part
        parts = clean_value.split('.')
        adjusted_parts = []

        for part in parts:
            try:
                int_part = int(part)
                if int_part > 255:
                    int_part = 255
                adjusted_parts.append(str(int_part))
            except ValueError:
                adjusted_parts.append(part)

        # Update the entry field with the adjusted value
        adjusted_value = ".".join(adjusted_parts)
        self.delete(0, "end")
        self.insert(0, adjusted_value)
        self.config(fg='#301934')  # Set text color to orange after validation
        self.typing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = LogInPageUI(root)
    root.mainloop()
