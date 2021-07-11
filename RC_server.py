import socket
import time
import XInput
from math import atan2, sqrt, pi, sin, cos

# HOST = "10.0.0.8"
HOST = "127.0.0.1"
PORT = 4210
CONTROLER_ID = 0
VOLTAGE_MULTIPLIER = 500
ROTATIONAL_VEL_CONST = 1
message = "hello ESP8266".encode()

class MotorController:
    def __init__(self):
        self.motorVel = [0.0,0.0,0.0,0.0]
        self.velocities = [0.0,0.0,0.0] # [lin_Vel, theta, rotational_vel]
        self.message = "no message"
        print("controller initialized")

    def update(self):
        #get controller commands
        state = XInput.get_state(CONTROLER_ID)
        thumb_stick_vals = XInput.get_thumb_values(state)
        self.velocities[0] = sqrt(thumb_stick_vals[0][0]**2 + thumb_stick_vals[0][1]**2)
        self.velocities[1] = atan2(thumb_stick_vals[0][0],thumb_stick_vals[0][1])
        self.velocities[2] = thumb_stick_vals[1][0]*ROTATIONAL_VEL_CONST
        #print(self.velocities)

        # update motor velocities 
        self.motorVel[0] = VOLTAGE_MULTIPLIER*(self.velocities[0]*sin(self.velocities[1]+pi/4) + self.velocities[2]) 
        self.motorVel[1] = VOLTAGE_MULTIPLIER*(self.velocities[0]*cos(self.velocities[1]+pi/4) - self.velocities[2])
        self.motorVel[2] = VOLTAGE_MULTIPLIER*(self.velocities[0]*cos(self.velocities[1]+pi/4) + self.velocities[2])
        self.motorVel[3] = VOLTAGE_MULTIPLIER*(self.velocities[0]*sin(self.velocities[1]+pi/4) - self.velocities[2])
        
        self.message = "{},{},{},{}".format(self.motorVel[0],self.motorVel[1],self.motorVel[2],self.motorVel[3]).encode()
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("connected to:\nUDP IP: {}\nUDP PORT: {}\n".format(HOST,PORT))
controller = MotorController()

while True:
    try:
        controller.update()

        sock.sendto(controller.message, (HOST,PORT))
        # print(controller.message)
        time.sleep(0.01)
    except KeyboardInterrupt as kbe:
        print("keyboard interupt detected stopping controller")
        exit()

