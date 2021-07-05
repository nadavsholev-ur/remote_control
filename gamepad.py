import XInput
import time
import socket
controllers = XInput.get_connected()
print(controllers)

HOST = "10.0.0.9"
PORT = 44455

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print("connected to {}".format(HOST))

while(True):

    input_state = XInput.get_state(0)
    buttons = XInput.get_button_values(input_state)
    stick = XInput.get_thumb_values(input_state)
    str_stick = str(stick)
    sock.sendall(str_stick.encode())
    print(str_stick)
    time.sleep(0.01)
    