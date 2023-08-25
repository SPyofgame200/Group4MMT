from PIL import ImageGrab
import io

def capture_screen(client):
    INFO_SIZE = 100
    while client:
        image = ImageGrab.grab()
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        data = image_bytes.getvalue()
        
        # send frame size
        client.sendall(bytes(str(len(data)), "utf8"))

        # send frame data
        client.sendall(data)

        # listen to next command from client: continue or back
        check_stop = client.recv(INFO_SIZE).decode("utf8")
        if("STOP_RECEIVING" in check_stop):
            break