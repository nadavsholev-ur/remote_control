import XInput
import time
import socket
controllers = XInput.get_connected()
print(controllers)

HOST = "127.0.0.1"
PORT = 44555
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))
print("connected to server")

while(True):

    input_state = XInput.get_state(0)
    buttons = XInput.get_button_values(input_state)
    stick = XInput.get_thumb_values(input_state)
    stick_lst = [stick[0][0],stick[0][1],stick[1][0],stick[1][1]]
    stick_msg = str(round(stick[0][1],4)) + \
                "," + str(round(stick[0][0],4)) +\
                "," + str(round(stick[1][0],4)) + " "
    sock.sendall(stick_msg.encode())
    time.sleep(0.05)