import socket
from datetime import datetime
import random

class MercuryClient:

    def __init__(self):
        self.ip = "192.168.0.82"  # server IP address
        self.portnum = 1025
        
        self.buffer_size = 1024  # 受信するコマンドの最大バイト数(２のべき乗の値にする)

    def client_main(self, order):
        """
        サーバ(Raspberry pi)に命令を投げ、返り値を受け取る。
        返り値例
        DATE:20220221;TIME:16-31-52,TEMP:302.1;POW:120.3
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((self.ip, self.portnum))  # connect with server
            
            soc.sendall(order.encode())  # send order to server

            data = soc.recv(self.buffer_size).decode()  # get the data from server as string
        
        return data

    def get_data_from_mercury(self, order):
        data_string = self.client_main(order)  # ex) DATE:20220221,TIME:16-31-52,TEMP:302.1,POW:120.3
        data_dict = {}
        for content in data_string.split(","):
            _kind = content.split(":")[0]
            _value = content.split(":")[1]
            data_dict[_kind] = _value

        return data_dict

    def send_stop(self):
        return self.client_main(order="stop")
        





