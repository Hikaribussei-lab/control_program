from datetime import datetime
import socket
import time

import mercury_controller

class MercuryServer:
    """
    
    """
    
    def __init__(self):
        self.portnum = 1025
        self.ip_wired = "192.168.0.82"  #D206 server IP
        
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
                with connection:
                    quit_flag = False
                    while not quit_flag:
                        print("Waiting for client's order...")
                        client_command = connection.recv(self.buffer_size).decode()  # command from client PC.
                        if not client_command:
                            break
                        if client_command == "quit server":
                            quit_flag = 1
                            re = "Quit server."
                        elif client_command == "start mercury":
                            self.mc.connect_device()
                            re = "Start Mercury"
                        elif client_command == "stop":
                            re = self._stop_operations()
                        elif client_command == "quit mercury":
                            re = self._mercury_quit_operations()
                        else:
                            re = self._get_data_operations(client_command)

                        connection.sendall(re.encode())
                        
                        if quit_flag:
                            exit()

    def _get_data_operations(self, order):
        """
        クライアントPCからの命令に沿ったデータを取得し、文字列として返す。
        """
        orders = order.split(";")
        
        now = datetime.now()
        snow = now.strftime('%Y/%m/%d %H-%M-%S')
        sdate = snow.split(" ")[0]
        stime = snow.split(" ")[1]
        
        get_time = time.time()  # UNIX時間
        
        datas = [f"DATE:{sdate}", f"TIME:{stime}", f"GETTIME:{get_time}"]
        
        if "TEMP" in orders:
            _temp = self.mc.get_temperature()
            datas.append(f"TEMP:{_temp}")
        
        if "POW" in orders:
            _pow = self.mc.get_power()
            datas.append(f"POW:{_pow}")
        
        data_string = ",".join(datas)
        
        return data_string
    
    def _stop_operations(self):
        return_string = "Connection with Mercury is closed."
        print(return_string)

        return return_string
    
    def _mercury_quit_operations(self):
        self.mc.device.close()
        self.mc.rm.close()
        return_string = "Quit Mercury."
        print(return_string)
        
        return return_string

if __name__ == "__main__":
    ms = MercuryServer()
    ms.server_setup()
