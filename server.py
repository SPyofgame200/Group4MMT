import tkinter as tk
import subprocess
import remote_key_logger_server as rkls
import list_apps_processes_server as aps
import capture_screen_server as css
import shutdown_logout_server as sls
from constant import *
import pyperclip
import socket
import threading  # Import the threading module

# Initialize Tkinter
main = tk.Tk()
main.geometry("250x250")
main.title("Server")
main['bg'] = '#000000'

def execute_client_command(client, command):
    """
    Thực thi lệnh của khách hàng dựa trên loại lệnh
    """
    if "KEYLOG" in command:
        rkls.keylog(client)
    elif "SD_LO" in command:
        sls.shutdown_logout(client)
    elif "CAPTURE_SCREEN" in command:
        css.capture_screen(client)
    elif "APP_PRO" in command:
        aps.apps_proccesses(client)
    elif "QUIT" in command:
        return False
    return True

def get_local_ipv4_address():
    """
    Lấy địa chỉ IPv4 cục bộ của máy và cập nhật nút "OPEN"
    """
    try:
        output = subprocess.check_output(['ipconfig']).decode('utf-8')
        lines = output.splitlines()
        found_adapter = False
        for line in lines:
            if 'Wireless LAN adapter Wi-Fi' in line:
                found_adapter = True
            elif found_adapter and 'IPv4 Address' in line:
                host = line.split(':')[-1].strip()
                open_button.config(text=host)
                # Copy the IP address to the clipboard
                pyperclip.copy(host)
                return
        if not found_adapter:
            open_button.config(text="Adapter Not Found")
        else:
            open_button.config(text="IP Not Found")
    except subprocess.CalledProcessError:
        open_button.config(text="Error")

def connect_and_listen():
    """
    Tạo kết nối socket và lắng nghe các tin nhắn khách hàng đến.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, SERVER_PORT))
    server_socket.listen(100)

    client, addr = server_socket.accept()

    while True:
        client_message = client.recv(BUFFER_SIZE).decode("utf8")
        should_continue = execute_client_command(client, client_message)
        if not should_continue:
            client.close()
            server_socket.close()
            break

def open_button_clicked():
    # First, get and display the local IPv4 address
    get_local_ipv4_address()
    # Then, start listening for connections in a separate thread
    listener_thread = threading.Thread(target=connect_and_listen)
    listener_thread.start()

open_button = tk.Button(main, text="OPEN", width=15, height=3, fg='white', bg='IndianRed3', borderwidth=0,
          highlightthickness=0, command=open_button_clicked, relief="flat")
open_button.place(x=125, y=125, anchor="center")

main.mainloop()
