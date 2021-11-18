import socket
from datetime import datetime as dt

#  for socket communication
portnum = 1025
ip_wired = "192.168.11.20"  #serverIP


if __name__ == '__main__':
    print("Ready")
    while True:
        command = input("Command:")
        if command[0] == 'S':
            print("waiting")
        if command == 'C':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((ip_wired, portnum))
                s.listen(10)
                quitFlag = False
                filename = None
                print("Waiting for connection... ")
                while not quitFlag:
                    connection, address = s.accept()
                    with connection:
                        while not quitFlag:
                            data = connection.recv(1024)
                            if not data:
                                break
                            command = data.decode()
                            tdatetime = dt.now() 
                            string = "Command from the client:{}".format(command)+ " " + tdatetime.strftime("%Y/%m/%d %H:%M:%S")
                            print(string)
                            if command == "measure":
                                print("do it")
        if command == 'Q':
            break
        else:
            pass
