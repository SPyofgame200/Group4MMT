import os
from constant import *

def shutdown_logout(client):
    while True:
        message = client.recv(BUFFER_SIZE).decode(ENCODE_FORMAT)
        if "SHUTDOWN" in message:
            os.system('shutdown -s -t 10')
        elif "LOGOUT" in message:
            os.system('shutdown -l')
        return
    