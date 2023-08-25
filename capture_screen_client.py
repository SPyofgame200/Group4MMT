from threading import Thread
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import Frame
from tkinter.filedialog import asksaveasfile

BUFFSIZE = 1024 * 4

class DesktopScreen(Frame):
    def __init__(self, parent, client):    
        super().__init__(parent)
        self.setup_ui(parent)
        self.client = client
        self.status = True
        self.on_save = False
        self.start_receiving_images()

    def setup_ui(self, parent):
        """Setup the UI elements"""
        self.configure(bg="#008080", height=600, width=1000, bd=0, highlightthickness=0, relief="ridge")
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        self.setup_image_label()
        self.setup_save_button()
        self.setup_back_button()

    def setup_image_label(self):
        """Setup the label to display images"""
        self.image_label = tk.Label(self)
        self.image_label.place(x=20, y=0, width=960, height=540)

    def setup_save_button(self):
        """Setup the save button"""
        self.save_button = self.create_button('Save', self.save_image, x=320, y=560)

    def setup_back_button(self):
        """Setup the back button"""
        self.back_button = self.create_button('Back', self.stop_receiving_images, x=630, y=560)

    def create_button(self, text, command, x, y):
        """Create a standard button with hover and click effects"""
        button = tk.Button(self, text=text, bg="#00CED1", fg="#FFFFFF", font="arial 10 bold", command=command, relief="flat")
        button.place(x=x, y=y, width=50, height=30)

        # Add hover effect
        button.bind("<Enter>", lambda event, button=button: self.on_button_hover(event, button))
        button.bind("<Leave>", lambda event, button=button: self.on_button_leave(event, button))

        return button

    def on_button_hover(self, event, button):
        """Button hover effect"""
        button.config(bg="#20B2AA", fg="#FFFFFF")

    def on_button_leave(self, event, button):
        """Button leave effect"""
        button.config(bg="#00CED1", fg="#FFFFFF")

    def start_receiving_images(self):
        """Start receiving images from the server"""
        self.start = Thread(target=self.receive_images, daemon=True)
        self.start.start()

    def receive_images(self):
        """Continuously receive images from the server"""
        while self.status:            
            size = int(self.client.recv(100))

            data = b""
            while len(data) < size:
                packet = self.client.recv(999999)
                data += packet

            self.display_image(data)
            self.check_save_command(data)
            self.check_stop_command()


    def display_image(self, data):
        """Display received image"""
        image_pil = Image.open(io.BytesIO(data)).resize((960, 540), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(image_pil)
        self.image_label.configure(image=image_tk)
        self.image_label.image = image_tk

    def check_save_command(self, data):
        """Check if save command is activated"""
        if self.on_save:
            self.frame = data
            self.save_img()
            self.on_save = False

    def check_stop_command(self):
        """Check if stop command is activated"""
        if self.status:
            self.client.sendall(bytes("NEXT_FRAME", "utf8"))
        else:
            self.client.sendall(bytes("STOP_RECEIVING", "utf8"))
            self.destroy()

    def stop_receiving_images(self):
        """Stop receiving images from the server"""
        self.status = False

    def save_image(self):
        """Activate save image command"""
        self.on_save = True

    def save_img(self):
        """Save the current image"""
        if self.frame == None:
            return
        types = [('Portable Network Graphics', '*.png'), ('All Files', '*.*')]
        image_file = asksaveasfile(mode='wb', filetypes=types, defaultextension='*.png')
        if image_file is None:
            return
        image_file.write(self.frame)
