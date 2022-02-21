import serial
import sockets
import pyvisa as visa
import time

ip="192.168.0.208"
port=7020
usb="ASR"
r=visa.ResourceManager()

#temperature
def connect_device(s):
    dev = r.open_resource(s)
    dev.read_termination = '\n'
    dev.write_termination = '\n'
    return dev

#temperature
def get_temp(s):# s is device (inst)
    s.write("READ:DEV:MB1.T1:TEMP:SIG:TEMP")
    time.sleep(0.01)
    temp=inst.read()
    return temp

#power
def get_pow(s):# s is device (inst)
    s.write("READ:DEV:MB0.H1:HTR:SIG:POWR")
    time.sleep(0.01)
    pow=inst.read()
    return pow

if __name__ == "__main__":
    nm = "TCPIP::" + ip + "::" + str(port) + "::SOCKET"
    inst = connect_device(nm)
    for num in range(100):
        data=get_temp(inst)
        temp=data.replace("STAT:DEV:MB1.T1:TEMP:SIG:TEMP:", "").replace("K", " K")
        data = get_pow(inst)
        pow = data.replace("STAT:DEV:MB0.H1:HTR:SIG:POWR:", "").replace("W", " W")
        print(num, temp, pow)
    inst.close()
    r.close()