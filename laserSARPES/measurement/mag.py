# モジュールのインポート
import sys
import socket
import datetime
import time

args = sys.argv
ip = "192.168.10.55"
port = 7777
buff = 16000

def check_status(str):
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.connect((ip, port))
	msg=str+"\n"
	s1.send(msg.encode())
	time.sleep(0.1)
	data =s1.recv(buff).decode("utf-8")
	s1.close()
	return data

def change(str):
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.connect((ip, port))
	msg=str+"\n"
	s1.send(msg.encode())
	s1.close()

if __name__ == '__main__':
	ch = check_status("CH?").replace("CH:", "").rstrip()
	#print(ch)
	pol = check_status("POL?").replace("POL:", "").rstrip()
	#print(pol)
	mod = check_status("MODE?").replace("MODE:", "").rstrip()
	#print(mod)
	#t = check_status("TIMESET?").rstrip()
	#print(t)

	if mod != "AUTO":
		change("MODE:AUTO")
	
	if ch != args[1]:
		s = "CH:"+args[1]
		change(s)
	
	if pol != args[2]:
		s = "POL:"+args[2]
		change(s)
	change("CHAG:S")
	time.sleep(3.0)
	change("DSCHAG")
	
	

