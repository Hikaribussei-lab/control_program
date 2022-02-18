import sys
import socket
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
#from PIL import Image
ip = "192.168.0.201"
portnum = 1025
def move():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "move_stage"
    s.sendall(command.encode())
    data = s.recv(1024)
    print(repr(data.decode()))
def volt():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "volt"
    s.sendall(command.encode())
    data = s.recv(1024)
    volt=float(data.decode())
    data = s.recv(1024)
    var = float(data.decode())
    print ("電圧:{}".format(volt))
    print("分散:{}".format(var))
    return volt

def ask_number():
    print ("what's the start number of pulse?")

volt_list = []
x_list = []
pulse = 0
if __name__ == '__main__':
    print("Ready")
    while pulse == 0:
        num_pulse = input("What's the start number of pulse?")
        print (num_pulse)
        pulse = num_pulse

    for num in range(64):
        #volt()
        volt_list.append(volt())
        time.sleep(1)
        move()
        x_list.append((num*(-1000) + int(pulse)) * 0.0025)

    plt.plot(x_list, volt_list)
    plt.show()
    print (volt_list)













