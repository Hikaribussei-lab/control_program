import sys
import socket
from datetime import datetime

ip = "192.168.11.20"#sever ip
portnum = 1025

if __name__ == '__main__':
    print("Ready")
    while True:
        command = input()
        if command == "Q":
            break
        if command == "S":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "measure"
                s.sendall(command.encode())
        else:
            print("only use S")

