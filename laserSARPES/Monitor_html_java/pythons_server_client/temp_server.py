import random
import time
import datetime
import socket, pickle
from lakeshore.model_335 import *
import time
import itertools

ip = '192.168.10.205'
portnum = 1234
buffer_size=4096

def get_temp_lakeshore():
    my_model_335 = Model335(57600)
    temperature_reading = my_model_335.get_all_kelvin_reading()
    # Open a csv file to write
    #file = open("335_record_data.csv", "w")
    # Write the data to the file
    print ("Data retrieved from the Lake Shore Model 335")
    #print("Temperature Reading A: " + str(temperature_reading[0]) + "\n")
    #print("Temperature Reading B: " + str(temperature_reading[1]) + "\n")
    #print("Heater Output 1: " + str(heater_output_1) + "\n")
    #print("Heater Output 2: " + str(heater_output_2) + "\n")
    return temperature_reading[0], temperature_reading[1]


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, portnum))
        s.listen(10)
        quitFlag = 0
        print("waiting for connection from client")
        while not quitFlag:
            connection, address = s.accept()
            with connection:
                quit_flag = False
                while not quit_flag:
                    # command from intermediate PC.
                    client_command = connection.recv(buffer_size).decode()
                    if not client_command:
                        break
                    if client_command == "Get":
                        try:
                            temp1, temp2 = get_temp_lakeshore()
                            data = [temp1, temp2]
                            print(datetime.datetime.now(),data)
                        except:
                            print("lakeshore connection faild")
                            pass
                            #data = [0, 0]
                        
                        try:
                            msg = pickle.dumps(data)
                            connection.sendall(msg)
                        except:
                            print("connetion faild")
                            pass
