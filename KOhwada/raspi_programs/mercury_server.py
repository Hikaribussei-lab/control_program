from datetime import datetime as dt
import socket

import random

import mercury_controller

class MercuryServer:
    """
    
    """
    
    def __init__(self):
        self.portnum = 1025
        self.ip_wired = "192.168.11.71"  #serverIP
        
        self.buffer_size = 1024  # 受信するコマンドの最大バイト数(２のべき乗の値にする)
        
        self.mc = mercury_controller.MercuryController()
    
    def server_setup(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip_wired, self.portnum))
            s.listen(10)
            
            quitFlag = 0
            print("Waiting for connection... ")
            while not quitFlag:
                connection, address = s.accept()
                print("Waiting for client's order...")
                with connection:
                    quit_flag = False
                    while not quit_flag:
                        client_command = connection.recv(self.buffer_size).decode()  # command from client PC.
                        if not client_command:
                            break
                        tdatetime = dt.now() 
                        string = f"Command from the client:{client_command} {tdatetime.strftime('%Y/%m/%d %H-%M-%S')}"
                        print(string)
                        if client_command == "quit":
                            quit_flag = 1
                        else:
                            data = self._server_operations(client_command)
                            connection.sendall(data.encode())
                            print(data)
                        
    
    def _server_operations(self, client_command):
        """
        クライアントPCからの命令に沿ったデータを取得し、文字列として返す。
        """
        if client_command == "random":                    
            data = self.mc.randomtest()
            
        elif client_command == "constant":
            data = self.mc.constanttest()
        
        elif client_command == "time":
            data = self.mc.timetest()
     
        return data


if __name__ == "__main__":
    ms = MercuryServer()
    ms.server_setup()