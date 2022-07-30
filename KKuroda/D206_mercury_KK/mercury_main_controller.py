from datetime import datetime
import socket
import time
import pyvisa as visa

import mercury_controller_calibrate as mc

ip = "192.168.0.208"  # Mercury's IP address
port = 7020


if __name__ == "__main__":
    rm = visa.ResourceManager()
    nm = f"TCPIP::{ip}::{port}::SOCKET"
    device = rm.open_resource(nm)
    device.read_termination = '\n'
    device.write_termination = '\n'
    for i in range(1000):
        device.write("READ:DEV:MB1.T1:TEMP:SIG:TEMP")
        time.sleep(0.01)
        temp = device.read()
        temp = temp.replace("STAT:DEV:MB1.T1:TEMP:SIG:TEMP:", "").replace("K", "")
        time.sleep(0.01)
        device.write("READ:DEV:DB1.T1:TEMP:SIG:RES")
        time.sleep(0.01)
        res = device.read()
        res = res.replace("STAT:DEV:DB1.T1:TEMP:SIG:RES:", "").replace("Ohm", "")
        print(temp, res)
        time.sleep(2)
        i+=1