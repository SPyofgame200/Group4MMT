import tkinter as tk
from tkinter import  ttk
import pickle, struct
from tkinter import*
from PIL import Image, ImageTk
import os
import sys

BUFFER_SIZE = 1024 * 4

def get_absolute_path(file_name):
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, file_name)

def receive_all(sock, size):
    message = bytearray()
    while len(message) < size:
        buffer = sock.recv(size - len(message))
        if not buffer:
            raise EOFError('Không thể nhận được toàn bộ thông tin cần tìm!')
        message.extend(buffer)
    return bytes(message)

def receive_data(client):
    packed = receive_all(client, struct.calcsize('!I'))
    size = struct.unpack('!I', packed)[0]
    data = receive_all(client, size)
    return data

def switch_display_mode(button, tab):
    text = 'APPLICATION' if button['text'] == 'PROCESS' else 'PROCESS'
    button.configure(text=text)
    tab.heading("Name", text=f"NAME {text}")
    tab.heading("ID", text=f"ID {text}")
    tab.heading("Count", text="COUNT THREADS")

def clear_tab(tab):
    for i in tab.get_children():
        tab.delete(i)

def terminate_process(client, pid):
    client.sendall(bytes("0", "utf8"))
    client.sendall(bytes(str(pid.get()), "utf8"))
    message = client.recv(BUFFER_SIZE).decode("utf8")
    if "1" in message:
        tk.messagebox.showinfo(message="Tiến trình kết thúc thành công!")
    else:
        tk.messagebox.showerror(message="Lỗi!")

def list_app_proccess(client, tab, s):
    client.sendall(bytes("1", "utf8"))
    client.sendall(bytes(s, "utf8"))

    list1 = pickle.loads(receive_data(client))
    list2 = pickle.loads(receive_data(client))
    list3 = pickle.loads(receive_data(client))

    clear_tab(tab)
    for i in range(len(list1)):
        tab.insert(parent='', index='end', text='', values=(list1[i], list2[i], list3[i]))


def start_process(client, process_name):
    client.sendall(bytes("3", "utf8"))
    client.sendall(bytes(str(process_name.get()), "utf8"))

def create_start_window(root, client):
    start_window = tk.Toplevel(root)
    start_window['bg'] = 'black'
    start_window.geometry("420x50")
    process_name = tk.StringVar(start_window)
    tk.Entry(start_window, textvariable=process_name, width=38, borderwidth=5).place(x=8, y=20)
    tk.Button(start_window, text="Start", width=14, height=2, fg='white', bg='IndianRed3', borderwidth=0,
              highlightthickness=0, command=lambda: start_process(client, process_name), relief="flat").place(x=300, y=15)

def create_kill_window(root, client):
    kill_window = tk.Toplevel(root)
    kill_window['bg'] = '#B7C9E2'
    kill_window.geometry("420x50")
    pid = tk.StringVar(kill_window)
    tk.Entry(kill_window, textvariable=pid, width=38, borderwidth=5).place(x=8, y=20)
    tk.Button(kill_window, text="Kill", width=14, height=2, fg='white', bg='IndianRed3', borderwidth=0,
              highlightthickness=0, command=lambda: terminate_process(client, pid), relief="flat").place(x=300, y=15)


class AppProcessUI(Frame):
    def __init__(self, parent, client):    
        Frame.__init__(self, parent)
        self.configure_window(parent)
        self.configure_background()
        self.treeview = self.configure_treeview()
        self.configure_buttons(parent, client)

    def configure_window(self, parent):
        self.configure(bg="#B7C9E2", height=600, width=1000, bd=0, highlightthickness=0, relief="ridge")
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")

    def configure_background(self):
        self.background_image = ImageTk.PhotoImage(Image.open(get_absolute_path("bg8.png")))
        self.background_label = Label(self, image=self.background_image, bg='#B7C9E2')
        self.background_label.pack(fill=X)

    def configure_treeview(self):
        treeview = ttk.Treeview(self, height = 18, selectmode='browse')
        scrollbar = tk.Scrollbar(self, orient = "vertical", command = treeview.yview)
        scrollbar.place(x=850, y=40, height=404)
        treeview.configure(yscrollcommand = scrollbar.set)
        treeview['columns'] = ("Name", "ID", "Count")
        treeview.column('#0', width=0)
        treeview.column("Name", anchor="center", width = 150, minwidth = 10, stretch = True)
        treeview.column("ID", anchor="center", width = 150, minwidth = 10, stretch = True)
        treeview.column("Count", anchor="center", width = 150, minwidth = 10, stretch = True)
        treeview.heading('#0', text='')
        treeview.heading("Name", text = "Name Application")
        treeview.heading("ID", text = "ID Application")
        treeview.heading("Count", text = "Count Threads")
        treeview.place(x=140, y=40, width=713, height=404)
        return treeview

    def create_button(self, text, command, x, y):
        button = Button(self, text=text, width=20, height=5, fg='white', bg='IndianRed3',
                        borderwidth=0, highlightthickness=0, command=command, relief="flat")
        button.place(x=x, y=y, width=135, height=50)
        return button

    def configure_buttons(self, parent, client):
        self.button_process = self.create_button('PROCESS', lambda: switch_display_mode(self.button_process, self.treeview), 80, 460)
        self.button_list = self.create_button('LIST', lambda: list_app_proccess(client, self.treeview, self.button_process['text']), 80, 520)
        self.button_start = self.create_button('START', lambda: create_start_window(parent, client), 450, 460)
        self.button_kill = self.create_button('KILL', lambda: create_kill_window(parent, client), 450, 520)
        self.button_clear = self.create_button('CLEAR', lambda: clear_tab(self.treeview), 820, 460)
        self.button_back = self.create_button('BACK', None, 820, 520)