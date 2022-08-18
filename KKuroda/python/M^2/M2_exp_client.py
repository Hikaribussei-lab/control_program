import sys
import socket
from datetime import datetime
import numpy as np
import time
from PIL import Image

ip = "192.168.0.202"
portnum = 1025


def take_picture():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "measure"
    s.sendall(command.encode())
    data = s.recv(1024)
    print(repr(data.decode()))
    s.close()

def send_picture():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "send"
    s.sendall(command.encode())
    data = s.recv(1024)
    if data.decode() == "NG":
        print("failed.")
        print("Receiving a file...", end="")
    sys.stdout.flush()
    with open("received.npy", "wb") as f:
        data = s.recv(1024)
        while data:
            f.write(data)
            data = s.recv(1024)
            if len(data) == 0:
                break
    array = np.load("received.npy")
    filename = datetime.now().strftime("Img_%Y%m%d_%H%M%S.png")
    img = Image.fromarray((array / 4).astype(np.uint8))
    img.save(filename)
    print("Done!")
    s.close()
    
def move_stage():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "move_stage"
    s.sendall(command.encode())
    data = s.recv(1024)
    print(repr(data.decode()))
    s.close()

def move_stage_home():
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "move_stage_home"
    s.sendall(command.encode())
    data = s.recv(1024)
    print(repr(data.decode()))
    s.close()

def change_step(step):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "step"+str(step)
    s.sendall(command.encode())
    data = s.recv(1024)
    print(repr(data.decode()))
    s.close()

if __name__ == '__main__':
    print("Ready")
    move_stage_home()
    time.sleep(0.5)
    #put intial pos
    change_step(500)
    time.sleep(0.5)
    move_stage()
    #put move step
    step = 100
    change_step(step)
    time.sleep(0.5)
    #range
    total_step = 0
    while total_step < 20000:
        move_stage()
        time.sleep(0.5)
        take_picture()
        time.sleep(0.5)
        send_picture()
        total_step += step