import time
import datetime
import sys
import requests
import socket, pickle
import commu_with_AIO as cm
from PyExpLabSys.PyExpLabSys.drivers.pfeiffer import TPG261

ip = "192.168.10.205"#sever ip
portnum = 1234

ip_ape_pulse = "192.168.10.4"#sever ip
portnum_ape_pulse = 2345

def post_thingspeak(value1, value2, value3, value4, value5, value6, value7):
	url = 'https://api.thingspeak.com/update'
	thingspeak_api_key = '7TG7H5JFNBMLAQXX'
	params = {
		'api_key': thingspeak_api_key,
		'field1': value1, # main_pressure
		'field2': value2, # prep_pressure
		'field3': value3, # vprep_pressure
        'field4': value4, # ll_pressure
        'field5': value5, # cryo_temp
		'field6': value6, # sample_temp
        'field7': value7 # pulse
	}
	r = requests.get(url, params=params)
	return r.status_code

def press_from_pfeiffer_serial():
    tpg = TPG261(port='/dev/ttyUSB0')
    v = tpg.pressure_gauges()
    print(v)

def temp_from_Lakeshore_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.connect((ip, portnum))
        command = "Get"
        try:
            sc.sendall(command.encode())
            time.sleep(1)
            data = sc.recv(4096)
            #print(len(data))
            data_arr = pickle.loads(data)
            return data_arr
        except:
            print("socket connetion faild")
            pass
        sc.close()
        
def pulsewidth_from_APE_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.connect((ip_ape_pulse, portnum_ape_pulse))
        sc.settimeout(5)
        command = "Get"
        try:
            sc.sendall(command.encode())
            time.sleep(1)
            data = sc.recv(1024).decode()
            #print(data)
            return data 
        except socket.timeout:
            print("タイムアウトエラー: サーバからの応答がありませんでした")
        except socket.error as e:
            print("socket connetion faild")
            data = "0"
            pass  
        finally:
            sc.close()
        


if __name__ == '__main__':
    while True:
        try:
            data = cm.get_pressure()
            temp = temp_from_Lakeshore_server()
            pulse = pulsewidth_from_APE_server()
            #print(pulse)
            #print(temp[0], temp[1])
            p = post_thingspeak(
                '{:.12f}'.format(data[0]),
                '{:.12f}'.format(data[1]),
                '{:.12f}'.format(data[2]),
                '{:.12f}'.format(data[3]),
                '{:.3f}'.format(temp[0]),
                '{:.3f}'.format(temp[1]),
                pulse
                )
            print(datetime.datetime.now(), "ThingSpeak : %d" % (p))
        except KeyboardInterrupt:
            pass
        
        time.sleep(15)