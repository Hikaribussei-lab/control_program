import subprocess
import socket
import datetime

#  for socket communication
portnum = 13517
ip_wired = "192.168.0.120"  # This PC

if __name__ == '__main__':
    print("Ready")
    quitFlag = False
    while not quitFlag:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip_wired, portnum))
            s.listen()
            print("Waiting for connection... ")
            while True:
                connection, address = s.accept()
                with connection:
                    data_bytes = connection.recv(1024)
                    command = data_bytes.decode()
                    now = datetime.datetime.now()
                    print(now.strftime("%Y/%m/%d %H:%M:%S") + " Command : {}".format(command))
                    # SES : SES activation and Ctr+G
                    if command == "SES":
                        try:
                            subprocess.call('C:/Users/LabComputer/Desktop/auto_program/ses_activate.exe', timeout=5)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Maybe : SES.exe is not opened.')
                            connection.sendall(b'Error!! Maybe : SES.exe is not opened.')
                    # ChB : Change to VLEED Black Ch.
                    elif command == "ChB":
                        try:
                            subprocess.call('C:/Users/LabComputer/Desktop/auto_program/Change_channel_black.exe', timeout=5)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Maybe : Spin Switch Control window is closed.')
                            connection.sendall(b'Error!! Maybe : Spin Switch Control window is closed.')
                    # ChW : Change to VLEED White Ch.
                    elif command == "ChW":
                        try:
                            subprocess.call('C:/Users/LabComputer/Desktop/auto_program/Change_channel_white.exe', timeout=5)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Maybe : Spin Switch Control window is closed.')
                            connection.sendall(b'Error!! Maybe : Spin Switch Control window is closed.')   
                    # DA30 X +OO.OO Y -OO.OO : Change theta of DA30
                    elif command[0:4] == "DA30":
                        process = 'C:/Users/LabComputer/Desktop/auto_program/AutoHotkey.exe'
                        cx = command.find('X')
                        cy = command.find('Y')
                        process += ' ' + str(float(command[cx+1:cy])) + ' ' + str(float(command[cy+1:]))
                        try:
                            subprocess.call(process, timeout=5)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Maybe : Control Theta window is closed.')
                            connection.sendall(b'Error!! Maybe : Control Theta window is closed.')
		    # X + or X - or Y + or Y - or Z1 + or Z1 - or Z2 + or Z2 - : Spin controll
                    elif command == 'X +' or command == 'X -' or command == 'Y +' or command == 'Y -' or command == 'Z1 +' or command == 'Z1 -' or command == 'Z2 +' or command == 'Z2 -':
                        process = 'C:/Users/LabComputer/Desktop/auto_program/spin_coil_command ' + command + ' 2'
                        try:
                            subprocess.call(process, timeout=30)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Spin controll ERROR.')
                            connection.sendall(b'Error!! Spin controll ERROR.')
                    elif command[0:5] == "Polar":
                        try:
                            subprocess.call('C:/Users/LabComputer/Desktop/auto_program/control_gonio_polar.exe' + command[5:], timeout=5)
                            connection.sendall(b'OK')
                        except subprocess.TimeoutExpired:
                            print('Error!! Maybe : jGonio_TF window is closed.')
                            connection.sendall(b'Error!! Maybe : jGonio_TF window is closed.')
                    # test : open notepad
                    elif command == "test":
                        subprocess.call('C:/Windows/system32/notepad.exe')
                        connection.sendall(b'OK')
                    # quit : Close this program
                    elif command == "quit":
                        connection.sendall(b'Bye!')
                        quitFlag = True
                        break
                    else:
                        connection.sendall(b'NG')
                        print("Wrong command!!")
