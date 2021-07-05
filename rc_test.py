import socket
import time
import XInput
from math import atan2, sqrt, pi, sin, cos

HOST = "10.0.0.8"
PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "hello".encode()
while True:
    try:
        sock.sendto(message, (HOST,PORT))
    except KeyboardInterrupt:
        print("exiting")
        exit()


