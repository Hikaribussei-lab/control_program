# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# 時間・スピン分解 ARPES ライブラリ
#
# 標準ライブラリ
#
from __future__ import print_function

import os
import re
import time
import datetime
import subprocess
import logging
import socket
import numpy as np
import asyncio
import sys

#
# 追加ライブラリ
#
# ファイル・フォルダ監視用
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

gfile = "logfile_TrSARPES_20210908.txt"

#イベントハンドラ
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    #ファイルやフォルダが作成された場合
    def on_created(self, event):
        now = datetime.datetime.now()
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print(now.strftime('%Y-%m-%d %H:%M:%S ')+'%s was made.' % filename)
        with open(gfile, "a", encoding="utf-8") as f:
            f.write(now.strftime('%Y-%m-%d %H:%M:%S ')+'%s was made. ' % filename)
        self.observer.unschedule_all()
        self.observer.stop()


class ARPES():
    def __init__(self):
        #  for socket communication
        self.WatchFolder_ip = '192.168.10.3' # This PC
        self.WatchFolder_port = 40001
        self.LabComputer_ip = '192.168.10.2' # SES computer
        self.LabComputer_port = 13517
    
    def SendSocket_LabComputer(self, command):
        print('Send command : ' + command)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.LabComputer_ip, self.LabComputer_port))
            sock.sendall(command.encode())
            data = sock.recv(1024)
            print(repr(data.decode()))
    
    # ファイル監視
    def WatchingFolder_wait(self, target_dir):
        #起動ログ
        print('start watching the data folder')
        observer = Observer()
        event_handler = ChangeHandler(observer)
        observer.schedule(event_handler, target_dir, recursive=True)
        observer.start()
    
        try:
            while observer.is_alive():
                time.sleep(0.5)
        except KeyboardInterrupt:
                observer.unschedule_all()
                observer.stop()
        observer.join()
        print('ok')

    def SES(self):
        self.SendSocket_LabComputer('SES')
    
    def DA30(self, x, y):
        if x >= 0.00:
            x_str ='+' +  '{:04.02f}'.format(x)
        else:
            x_str ='{:04.02f}'.format(x)
        if y >= 0.00:
            y_str ='+' +  '{:04.02f}'.format(y)
        else:
            y_str ='{:04.02f}'.format(y)
        self.SendSocket_LabComputer('DA30' + ' X' + x_str + ' Y' + y_str)

    def mag(self, a, p, t):
        time.sleep(0.5)
        if a == 'X' or a == 'Y':
            st = 'python mag.py X ' + str(p) + ' ' + str(t)
        elif a == 'Z': 
            st = 'python mag.py Y ' + str(p) + ' ' + str(t)
        subprocess.call(st)

    def ARPESmap(self):
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

    def test(self):
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
    
    def SARPES(self, ax):
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

    def SARPES8(self, ax):
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

    def SARPES12(self, ax):
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '-', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')
        time.sleep(0.5)
        self.mag(ax, '+', '2')
        time.sleep(0.5)
        self.SES()
        time.sleep(0.5)
        self.WatchingFolder_wait('Z:')

    
    def DAxSpinMap(self, pol_start, pol_number, pol_step):
        # super().SendSocket_LabComputer('ChW')
        # super().SendSocket_LabComputer('Y +')
        # super().DA30(0,0)
        # time.sleep(0.2)
        #super().SendSocket_LabComputer('Y + 2')
        time.sleep(2)
        pol = pol_start
        time.sleep(0.5)
        self.mag('Y', '+', '2')
        time.sleep(0.5)
        for i in range(pol_number):
            x= pol
            y= -0.45
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            pol += pol_step
        time.sleep(0.5)
        self.mag('Y', '-', '2')
        pol = pol_start
        #-Y
        for i in range(pol_number):
            x= pol
            y= -0.45
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            pol += pol_step
            

    def DAxMap(self, pol_start, pol_number, pol_step):
        # super().SendSocket_LabComputer('ChW')
        # super().SendSocket_LabComputer('Y +')
        # super().DA30(0,0)
        # time.sleep(0.2)
        #super().SendSocket_LabComputer('Y + 2')
        time.sleep(0.5)
        self.mag('Y', '-', '2')
        time.sleep(2)
        pol = pol_start
        time.sleep(0.5)
        for i in range(pol_number):
            x= pol
            y= -0.45
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            pol += pol_step
        time.sleep(0.5)
        
    def DAxySpinMap(self, polx_start,polystart, polx_number, poly_number,polx_step, poly_step):
        # super().SendSocket_LabComputer('ChW')
        # super().SendSocket_LabComputer('Y +')
        # super().DA30(0,0)
        # time.sleep(0.2)
        #super().SendSocket_LabComputer('Y + 2')
        time.sleep(2)
        pol = pol_start
        time.sleep(0.5)
        self.mag('Z', '+', '2')
        time.sleep(0.5)
        for i in range(polx_number):
            for j in range(poly_number):
                x= polx_start + i*polx_step
                y= poly_start + j*poly_step
                #self.Polar(pol)
                self.DA30(x,y)
                time.sleep(0.2)
                print(str(x) + "__" + str(y))
                #+Y
                time.sleep(0.5)
                self.SES()
                self.WatchingFolder_wait('Z:')
                
        time.sleep(0.5)
        self.mag('Z', '-', '2')
        pol = pol_start
        #-Y
        for i in range(pol_number):
            x= pol
            y= -0.1
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            
            
    def DAxARPESMap(self, pol_start, pol_number, pol_step):
        pol = pol_start
        time.sleep(0.5)
        #self.mag('Y', '+', '2')
        time.sleep(0.5)
        for i in range(pol_number):
            x= pol
            y= 0.5
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            pol += pol_step

    def DAyMapping(self, tilt_start, tilt_number, tilt_step):
        tilt = tilt_start
        time.sleep(0.5)
        for i in range(tilt_number):
            x= 0
            y= tilt
            #self.Polar(pol)
            self.DA30(x,y)
            time.sleep(0.2)
            print(str(x) + "__" + str(y))
            #+Y
            time.sleep(0.5)
            self.SES()
            self.WatchingFolder_wait('Z:')
            tilt += tilt_step
            
    def repeat(self):
        self.PolarMapping(-10, 41, 0.5)
                          
