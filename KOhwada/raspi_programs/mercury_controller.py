import pyvisa as visa
import time

class MercuryController:
    """
    Mercuryをコントロールするための実行クラス。
    """

    def __init__(self):
        self.ip = "192.168.0.208"  # Mercury's IP address
        self.port = 7020
        self.usb = "ASR"
        self.rm = visa.ResourceManager()

        self.connect_device()
    
    def connect_device(self):
        """
        Mercuryと接続
        """
        nm = f"TCPIP::{self.ip}::{self.port}::SOCKET"
        self.device = self.rm.open_resource(nm)
        self.device.read_termination = '\n'
        self.device.write_termination = '\n'
    
    def get_temperature(self):
        """
        Mercuryに温度を出力するように命令
        """
        self.device.write("READ:DEV:MB1.T1:TEMP:SIG:TEMP")
        time.sleep(0.01)
        temp = self.device.read()
        temp = temp.replace("STAT:DEV:MB1.T1:TEMP:SIG:TEMP:", "")

        return temp
    
    def get_power(self):
        """
        Mercuryにパワーを出力するように命令
        """
        self.device.write("READ:DEV:MB0.H1:HTR:SIG:POWR")
        time.sleep(0.01)
        pow = self.device.read()
        pow = pow.replace("STAT:DEV:MB0.H1:HTR:SIG:POWR:", "")

        return pow
