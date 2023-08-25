import tkinter as tk

def send_command(client, command):
    """Gửi lệnh cụ thể tới máy khách."""
    client.sendall(bytes(command, "utf8"))

def close_application(window, client):
    """Gửi lệnh QUIT tới máy khách và đóng ứng dụng."""
    send_command(client, "QUIT")
    window.destroy()

def open_shutdown_logout_window(client, root):
    """Mở một cửa sổ mới với các tùy chọn TẮT MÀN HÌNH và ĐĂNG XUẤT."""
    window = tk.Toplevel(root)
    window.geometry("190x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: close_application(window, client))

    create_button(window, 'ĐĂNG XUẤT', '#4d4d4d', '#e64040', lambda: send_command(client, "LOGOUT"), 0)
    create_button(window, 'TẮT MÁY', '#cd5c5c', '#ffffff', lambda: send_command(client, "SHUTDOWN"), 1)


    window.mainloop()

def create_button(window, text, bg_color, fg_color, command, row):
    """Tạo một button với các thuộc tính được chỉ định và thêm nó vào cửa sổ."""
    button = tk.Button(window, text=text, width=20, height=2, fg=fg_color, bg=bg_color, 
                       command=command, padx=20, pady=20)
    button.grid(row=row, column=0)
