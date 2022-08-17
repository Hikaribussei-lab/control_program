import sys
import socket
from datetime import datetime

ip = "192.168.10.2"#sever ip
portnum = 1025

if __name__ == '__main__':
    print("Ready")
    while True:
        command = input()
        if command == "Q":
            break
        if command == "m":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, portnum))
                command = "ses"
                s.sendall(command.encode())
        else:
            print("only use S")

