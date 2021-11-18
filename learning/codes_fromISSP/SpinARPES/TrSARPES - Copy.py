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

#
# 追加ライブラリ
#
# ファイル・フォルダ監視用
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Sigma Delay Stage 用ライブラリ
import stage_fukushima_v3


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
        self.WatchFolder_ip = '192.168.0.110' # This PC
        self.WatchFolder_port = 40001
        self.LabComputer_ip = '192.168.0.120' # LabComputer
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
    
    def Mapping_Yline(self, y_start, y_end, y_step, x_offset):
        y_now = y_start
        while y_now <= y_end:
            self.DA30(x_offset, y_now)
            self.SES()
            self.WatchingFolder_wait('Y:')
            y_now += y_step
    
    def Mapping_Xline(self, x_start, x_end, x_step, y_offset):
        x_now = x_start
        while x_now <= x_end:
            self.DA30(y_offset, x_now)
            self.SES()
            self.WatchingFolder_wait('Y:')
            x_now += x_step
    
    def YSpin_Mapping_Xline(self, x_start, x_end, x_step, y_offset):
        x_now = x_start
        x_pos = [x_start]
        while x_now < x_end:
            x_now += x_step
            x_pos.append(x_now)
        print(x_pos)
        x_num = len(x_pos)
        print(x_num)

        self.SendSocket_LabComputer('ChW')
        time.sleep(2)

        for j in range(2):
            self.SendSocket_LabComputer('Y +')
            time.sleep(2)
            i = 0
            while i < x_num:
                self.DA30(x_pos[i], y_offset)
                self.SES()
                self.WatchingFolder_wait('Y:')
                i += 1
            
            self.SendSocket_LabComputer('Y -')
            time.sleep(2)
            i = 0
            while i < x_num:
                self.DA30(x_pos[i], y_offset)
                self.SES()
                self.WatchingFolder_wait('Y:')
                i += 1
            
            self.SendSocket_LabComputer('Y -')
            time.sleep(2)
            i = 0
            while i < x_num:
                self.DA30(x_pos[i], y_offset)
                self.SES()
                self.WatchingFolder_wait('Y:')
                i += 1
            
            self.SendSocket_LabComputer('Y +')
            time.sleep(2)
            i = 0
            while i < x_num:
                self.DA30(x_pos[i], y_offset)
                self.SES()
                self.WatchingFolder_wait('Y:')
                i += 1

    def Spin_Original_Sequence(self):
        self.SendSocket_LabComputer('ChW')
        time.sleep(2)

        for i in range(3):
            self.SendSocket_LabComputer('Z2 +')
            time.sleep(2)
            self.SES()
            self.WatchingFolder_wait('Y:')

            self.SendSocket_LabComputer('Z2 -')
            time.sleep(2)
            self.SES()
            self.WatchingFolder_wait('Y:')

            time.sleep(2)
            self.SES()
            self.WatchingFolder_wait('Y:')

            self.SendSocket_LabComputer('Z2 +')
            time.sleep(2)
            self.SES()
            self.WatchingFolder_wait('Y:')



     

    
class TimeARPES(ARPES):
    def __init__(self):
        super().__init__()
        self.stage = stage_fukushima_v3.DelayStageController('hellogoogle')
        #self.OneStepTime = 2*10^(-6)/(3*10^8)

    def DelayStageOpen(self,com):
        self.stage.openPass(com)
    
    def DelayStageClose(self):
        self.stage.closePass()
    
    def PowerScan(self, scan_num):
        now = time.time()
        for i in range(scan_num):
            #now = time.time()
            super().SendSocket_LabComputer('SES')
            super().WatchingFolder_wait('Y:')
            while True:
                flag = time.time()
                delta = (flag - now)/(i+1)
                if delta >= 60:
                    break
                else:
                    time.sleep(0.1)
    
    # move to absolute pulse step @ delay line
    def AbsPulseStep(self, pulse):
        self.stage.moterSwitch(1)
        self.stage.moveFunction(2, pulse)
        self.stage.waitOperationFinished(60)
        print(self.stage.Qcommand())

    # scan delay line on a one way (linear step)
    def ScanPulseStep_OneWay(self, pulse_start, pulse_step, pulse_num):
        self.stage.moterSwitch(1)
        self.stage.moveFunction(2, pulse_start)
        self.stage.waitOperationFinished(60)
        pos = self.stage.Qcommand()
        print(pos)
        super().SendSocket_LabComputer('SES')
        super().WatchingFolder_wait('Y:')
        with open(gfile, "a", encoding="utf-8") as f:
            f.write("Pos:" + pos[0] + "\n")
        for i in range(pulse_num):
            self.stage.moveFunction(1, pulse_step)
            self.stage.waitOperationFinished(20)
            pos = self.stage.Qcommand()
            print(pos)
            super().SendSocket_LabComputer('SES')
            super().WatchingFolder_wait('Y:')
            with open(gfile, "a", encoding="utf-8") as f:
                f.write("Pos:" + pos[0] + "\n")

    # scan delay line on a round trip (linear step)
    def ScanPulseStep_repeat(self, pulse_start, pulse_step, pulse_num, repeat_num):
        self.stage.moterSwitch(1)
        self.stage.moveFunction(2, pulse_start)
        self.stage.waitOperationFinished(60)
        for j in range(2*repeat_num):
            for i in range(pulse_num):
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")
                self.stage.moveFunction(1, ((-1)**j)*pulse_step)
                self.stage.waitOperationFinished(20)
            pos = self.stage.Qcommand()
            print(pos)
            super().SendSocket_LabComputer('SES')
            super().WatchingFolder_wait('Y:')
            with open(gfile, "a", encoding="utf-8") as f:
                f.write("Pos:" + pos[0] + "\n")

    # scan delay line on list
    def ScanPulseStep_list(self):
        self.stage.moterSwitch(1)
        pulse_pos = [-1000,-200,-100,0,50,100,150,200,250,300,350,400,450,500,550,600,700,800,900,1000,2000,3000,4000,5000]
        # self.stage.moveFunction(2, pulse_pos[0])
        # self.stage.waitOperationFinished(60),
        pulse_num = len(pulse_pos)
        print(pulse_num)
        for j in range(2):
            # 順方向
            for i in range(pulse_num):
                self.stage.moveFunction(2, pulse_pos[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")
            
            # 逆方向
            for i in range(pulse_num):
                self.stage.moveFunction(2, pulse_pos[pulse_num-i-1])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")
                # self.stage.sendCommand('M:1+P' + str(pulse_step))
                # self.stage.sendCommand('G')
    
    # スキャンし続け、日時とともに保存する
    def PowerStability(self, scannum):
        for j in range(scannum):
            super().SendSocket_LabComputer('SES')
            super().WatchingFolder_wait('Y:')
            dt_now = datetime.datetime.now()
            gfile = "C:/Users/laser/Documents/Programs/ChamberTemp/laserPower_log/logfile_11eVPESpower_20210817.txt"
            with open(gfile, "a", encoding="utf-8") as f:
                f.write(dt_now.strftime('%Y-%m-%d %H:%M:%S') + " " + str(j+1) + "\n")
    
    def ScanLinearStep(self, pulse_start, pulse_end, pulse_step, repeat_num):
        i = 1
        pulse_pos = [pulse_start]
        while pulse_pos[i] < pulse_end:
            pulse_pos.append(pulse_start + pulse_step * i)
            i += 1

        scan_num = len(pulse_pos)
        print(pulse_pos)
        print("list num = " + str(scan_num))
        print("all scan num = 2 * " + str(repeat_num) + " * " + str(scan_num) + " = " + str(2*repeat_num * scan_num))

        self.stage.moterSwitch(1)
        
        for j in range(repeat_num):
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_pos[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")

            pulse_rev = pulse_pos[::-1]
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_rev[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")
    
    def ScanLogStep(self, pulse_center, pulse_start, pulse_end, pulse_offset, pulse_linear, pulse_exp, repeat_num):
        i = 0
        pulse_pos_m = [int(pulse_center + pulse_offset)]
        while pulse_pos_m[i] >= pulse_start:
            pulse_pos_m.append(int(pulse_center + pulse_offset - pulse_linear*(i+1) - pulse_exp**(i+1)))
            i += 1
        
        i = 0
        pulse_pos_p = [int(pulse_center + pulse_offset + pulse_linear + pulse_exp)]
        while pulse_pos_p[i] <= pulse_end:
            pulse_pos_p.append(int(pulse_center + pulse_offset + pulse_linear*(i+2) + pulse_exp**(i+2)))
            i += 1

        pulse_pos = pulse_pos_m[::-1]
        pulse_pos.extend(pulse_pos_p)

        scan_num = len(pulse_pos)
        print(pulse_pos)
        print("list num = " + str(scan_num))
        print("all scan num = 2 * " + str(repeat_num) + " * " + str(scan_num) + " = " + str(2*repeat_num * scan_num))

        self.stage.moterSwitch(1)
        
        for j in range(repeat_num):
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_pos[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")

            pulse_rev = pulse_pos[::-1]
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_rev[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write("Pos:" + pos[0] + "\n")
        
    def ScanLogStep_ScanNum(self, pulse_center, pulse_start, pulse_end, pulse_offset, pulse_linear, pulse_exp, repeat_num):

        i = 0
        pulse_pos_m = [int(pulse_center + pulse_offset)]
        while pulse_pos_m[i] >= pulse_start:
            pulse_pos_m.append(int(pulse_center + pulse_offset - pulse_linear*(i+1) - pulse_exp**(i+1)))
            i += 1
        
        i = 0
        pulse_pos_p = [int(pulse_center + pulse_offset + pulse_linear + pulse_exp)]
        while pulse_pos_p[i] <= pulse_end:
            pulse_pos_p.append(int(pulse_center + pulse_offset + pulse_linear*(i+2) + pulse_exp**(i+2)))
            i += 1

        pulse_pos = pulse_pos_m[::-1]
        pulse_pos.extend(pulse_pos_p)

        scan_num = len(pulse_pos)
        print(pulse_pos)
        print("list num = " + str(scan_num))
        print("all scan num = 2 * " + str(repeat_num) + " * " + str(scan_num) + " = " + str(2*repeat_num * scan_num))

        time_pos = np.array(pulse_pos)
        time_pos = (time_pos - pulse_center)*0.1/15 # delay time (ps)
        print("\n delay time (ps)")
        np.set_printoptions(suppress=True, precision=3, floatmode='maxprec')
        print(time_pos)
        print("ok")

    def ScanLogStep_Spin(self, pulse_center, pulse_start, pulse_end, pulse_offset, pulse_linear, pulse_exp, repeat_num, magdir):
        i = 0
        pulse_pos_m = [int(pulse_center + pulse_offset)]
        while pulse_pos_m[i] >= pulse_start:
            pulse_pos_m.append(int(pulse_center + pulse_offset - pulse_linear*(i+1) - pulse_exp**(i+1)))
            i += 1
        
        i = 0
        pulse_pos_p = [int(pulse_center + pulse_offset + pulse_linear + pulse_exp)]
        while pulse_pos_p[i] <= pulse_end:
            pulse_pos_p.append(int(pulse_center + pulse_offset + pulse_linear*(i+2) + pulse_exp**(i+2)))
            i += 1

        pulse_pos = pulse_pos_m[::-1]
        pulse_pos.extend(pulse_pos_p)

        scan_num = len(pulse_pos)
        print(pulse_pos)
        print("list num = " + str(scan_num))
        print("all scan num = 4 * " + str(repeat_num) + " * " + str(scan_num) + " = " + str(4*repeat_num * scan_num))

        pulse_rev = pulse_pos[::-1]

        self.stage.moterSwitch(1)
        
        if magdir == 'X' or magdir == 'Z1':
            super().SendSocket_LabComputer('ChW')
            time.sleep(2)
        elif magdir == 'Y' or magdir == 'Z2':
            super().SendSocket_LabComputer('ChW')
            time.sleep(2)
        else:
            print("Magnet direction ERROR! : " + magdir)

        for j in range(repeat_num):
            super().SendSocket_LabComputer(magdir + ' +')
            time.sleep(2)
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_pos[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write(magdir + " + Pos:" + pos[0] + "\n")
            
            super().SendSocket_LabComputer(magdir + ' -')
            time.sleep(2)
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_rev[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write(magdir + " - Pos:" + pos[0] + "\n")
            
            super().SendSocket_LabComputer(magdir + ' -')
            time.sleep(2)
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_pos[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write(magdir + " - Pos:" + pos[0] + "\n")
            
            super().SendSocket_LabComputer(magdir + ' +')
            time.sleep(2)
            for i in range(scan_num):
                self.stage.moveFunction(2, pulse_rev[i])
                self.stage.waitOperationFinished(60)
                pos = self.stage.Qcommand()
                print(pos)
                super().SendSocket_LabComputer('SES')
                super().WatchingFolder_wait('Y:')
                with open(gfile, "a", encoding="utf-8") as f:
                    f.write(magdir + " + Pos:" + pos[0] + "\n")

    def ExitLabComputer(self):
        super().SendSocket_LabComputer('quit')
    
#################################################################################################
#Yuto Fukushima 
###################################################################################################
    def spin_SES(self):
        super().SES()
        super().WatchingFolder_wait('Y:')
        time.sleep(0.2)
        super().SendSocket_LabComputer('Y -')
        time.sleep(2)
        super().SES()
        super().WatchingFolder_wait('Y:')
        time.sleep(0.2)
        super().SES()
        super().WatchingFolder_wait('Y:')
        time.sleep(0.2)
        super().SendSocket_LabComputer('Y +')
        time.sleep(2)
        super().SES()
        super().WatchingFolder_wait('Y:')
        time.sleep(0.2)

    def YSpin_Polar_Mapping(self, pol_start, pol_number, pol_step):
        if pol_start> 60 or pol_number*pol_step+pol_start>60:
            print('Error Polar is out of range!!!')
            exit()
        
        # super().SendSocket_LabComputer('ChW')
        # super().SendSocket_LabComputer('Y +')
        # super().DA30(0,0)
        # time.sleep(0.2)
        super().SendSocket_LabComputer('Y +')
        time.sleep(2)
        pol = pol_start
        for i in range(pol_number):
            x=0
            y= -1.6603-0.066728*pol
            self.Polar(pol)
            super().DA30(x,y)
            time.sleep(0.2)
            print(str(pol) + "__" + str(x) + "__" + str(y))
            self.spin_SES()
            pol += pol_step


    def Spin_DA30_Mapping(self, x_start,x_step,x_num, y_start, y_end):         
    #def Spin_DA30_Mapping(self, x_start,x_end,y_num, y_step, y_start):

        y_step = (y_end-y_start)/(x_num-1)
        #x_step = (x_end-x_start)/(y_num-1)
        super().DA30(0,0)
        super().SendSocket_LabComputer('Y +')
        time.sleep(3)

        x=[x_start]
        y=[y_start]
        for i in range(x_num-1):
            x.append(x[i]+x_step)
            y.append(y[i]+y_step)
        print(x)
        print(y)
        x = x[::-1]
        y = y[::-1]

        for k in range(x_num):
            super().DA30(x[k],y[k])
            print(str(x[k])+'and'+str(y[k]))
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)

        super().SendSocket_LabComputer('Y -')
        time.sleep(3)
        for k in range(x_num):
            super().DA30(x[k],y[k])
            print(str(x[k])+'and'+str(y[k]))
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)
        for k in range(x_num):
            super().DA30(x[k],y[k])
            print(str(x[k])+'and'+str(y[k]))
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)

        super().SendSocket_LabComputer('Y +')
        time.sleep(3)
        for k in range(x_num):
            super().DA30(x[k],y[k])
            print(str(x[k])+'and'+str(y[k]))
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)

    def Spin_DA30_YMapping(self,x_offset, y_start, y_step,y_num):
        x=x_offset
        super().DA30(0,0)
        time.sleep(0.2)
        for k in range(y_num):
            super().DA30(x,y_start +k*y_step)
            print(str(x) + " and " + str(y_start +k*y_step))
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)

           

    def spin_repeat(self,num):
        super().SendSocket_LabComputer('Y +')
        time.sleep(3)

        for i in range(num):
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)
            super().SendSocket_LabComputer('Y -')
            time.sleep(3)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)
            super().SendSocket_LabComputer('Y +')
            time.sleep(3)
            super().SES()
            super().WatchingFolder_wait('Y:')
            time.sleep(0.2)

    def Polar(self, pol):
        super().SendSocket_LabComputer('Polar ' + str(pol))
        time.sleep(10)

