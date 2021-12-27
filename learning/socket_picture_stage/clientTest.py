import sys
import socket
from datetime import datetime
import numpy as np
import pickle
from PIL import Image

ip = "192.168.11.53"
portnum = 1025

if __name__ == '__main__':
    print("Ready")
    while True:
        command = input()
        if command == "Q":
            break
        if command == "M":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "move_stage"
                s.sendall(command.encode())
                data = s.recv(1024)
                print(repr(data.decode()))
        if command == "T":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "measure"
                s.sendall(command.encode())
                data = s.recv(1024)
                print(repr(data.decode()))
        if command == "S":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
                print(filename)
                img = Image.fromarray((array / 4).astype(np.uint8))
                img.save(filename)
                print("Done!")
        if command == "E":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "quit"
                s.sendall(command.encode())
                data = s.recv(1024)
                print(repr(data.decode()))
        if command[0] == "I":
            iso = int(command[1:])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "iso" + str(iso)
                s.sendall(command.encode())
                data = s.recv(1024)
                print(repr(data.decode()))
