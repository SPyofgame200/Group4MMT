from constant import *
import socket

# = = = = = # = = = = = # = = = = = # GLOBAL VARIABLES # = = = = = # = = = = = # = = = = = #

server_buffer = bytes()
server_user_count = 0

# = = = = = # = = = = = # = = = = = # BUFFER MANAGEMENT # = = = = = # = = = = = # = = = = = #

def receive_buffer(connector: socket):
    """
        fetch dữ liệu từ bên gửi
    """
    global server_buffer

    data_partition = connector.recv(BUFFER_SIZE)
    server_buffer += data_partition

def get_data(connector: socket):
    """
        header: 4 bytes
        |
        V 
        0012abcdefghijkl
                ^
                |
            content
        lấy các blockdata đến khi đủ thì trả về
    """
    global server_buffer 
    
    #* chờ tới khi lấy đủ header (mặc định là 4 bytes)
    split_position = 4
    while (len(server_buffer) < split_position):
        receive_buffer(connector)
        
    #* lấy header (aka độ dài content)
    data_size_str = server_buffer[:split_position]
    data_size = int.from_bytes(data_size_str, byteorder='big')
    
    #* xóa header (aka: data_size_str) từ buffer
    server_buffer = server_buffer[split_position:]

    #* chờ tới khi nhận đủ content
    while (len(server_buffer) < data_size):
        receive_buffer(connector)

    #* lấy thông tin content (mã hoá)
    content = server_buffer[:data_size]
    server_buffer = server_buffer[data_size:]
    
    #* dịch ngược lại thông tin
    data = (content).decode(ENCODE_FORMAT)
    return data