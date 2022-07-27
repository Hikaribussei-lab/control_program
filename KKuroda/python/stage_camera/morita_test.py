import sys
import socket
from datetime import datetime
import numpy as np
import pickle
import time
import tkinter
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt

from tkinter import filedialog
from tkinter import messagebox

ip = "192.168.0.202"
portnum = 1025




def move():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "move_stage"
    s.sendall(command.encode())
    jog = jog_var.get()
    s.sendall(jog.encode())
    data = s.recv(1024)
    u = repr(data.decode()).replace("moved >>> ", "")
    print(u)
    # return u

def rotate():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "rotate_stage"
    s.sendall(command.encode())
    deg = str(deg_var.get())
    s.sendall(deg.encode())
    data = s.recv(1024)
    data = float(data.decode())
    u = f"rotated >>> {data}"
    print(u)
    return data

def n_rotate():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "n_rotate_stage"
    s.sendall(command.encode())
    data = s.recv(1024)
    u = repr(data.decode()).replace("rotated >>> ", "")
    print(u)


def volt():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = "volt"
    s.sendall(command.encode())
    data = s.recv(1024)
    volt = float(data.decode())
    data = s.recv(1024)
    var = float(data.decode())
    print ("電圧:{}".format(volt))
    print("分散:{}".format(var))
    return volt

def initialize():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, portnum))
    command = 'initialize'
    s.sendall(command.encode())
    data = s.recv(1024)
    messagebox.showinfo('完了', data.decode())
    data = s.recv(1024)


def write_text(filenames, d_list, v_list, nums):
    with open(filenames, 'w') as f:
        for i in range(nums):
            f.write(str(d_list[i]))
            f.write(' ')
            f.write(str(v_list[i]))
            f.write('\n')



def get_path():
    idir = 'C:\\Users\\Takuma Iwata\\Desktop\\D206'
    filetype =[("すべて","*")]
    file_path = tkinter.filedialog.askdirectory(initialdir=idir)
    path_label.insert(tkinter.END, file_path)
    return file_path

def make_filename(filenames, samples):
    dt = datetime.datetime.now()
    return filenames + '/' + samples + '_' + dt.strftime('%Y%m%d%H%M') + '.txt'



def measure():
    volt_list = []
    x_list = []
    print("Ready")
#    while True:
#        num = int(input("How many times do you measure?"))
#        print (num*2)
#        if num:
#            break
    nums = num.get()
    for i in range(nums):
        #volt()
        volt_list.append(volt())
        time.sleep(0.5)
        x_list.append(rotate())
        time.sleep(0.5)
    for i in range(nums):
        print(x_list[i], volt_list[i]) # 2 is step
    filenames = make_filename(filename.get(), sample.get())
    write_text(filenames, x_list, volt_list, nums)
    plt.plot(x_list, volt_list)
    plt.show()





if __name__ == '__main__':
    print("Ready")

    # メインウィジェット
    main_win = tkinter.Tk()
    main_win.title('Controller')
    main_win.geometry('500x250')

    # メインフレーム
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

    # パラメーター
    jog_var = tkinter.IntVar()
    deg_var = tkinter.DoubleVar()
    filename = tkinter.StringVar()
    sample = tkinter.StringVar()
    num = tkinter.IntVar()

    # ウィジェット
    initialize_button = tkinter.Button(main_frm, text='Initialize', command=initialize)

    jog_label = ttk.Label(main_frm, text='StepMove')
    jog_box = ttk.Entry(main_frm, textvariable=jog_var)
    jog_button = ttk.Button(main_frm, text='Step move', command=move)

    rotate_label = ttk.Label(main_frm, text='StepRotate')
    rotate_box = ttk.Entry(main_frm, textvariable=deg_var)
    rotate_button = ttk.Button(main_frm, text='Step rotate', command=rotate)

    volt_label = ttk.Label(main_frm, text='Measure Volt')
    # volt_box = ttk.Entry(main_frm)
    # volt_box.insert(tkinter.END, deg_var.get())
    volt_button = ttk.Button(main_frm, text='Execute', command=volt)

    measure_label = ttk.Label(main_frm, text='Measure Volt')
    measure_box = ttk.Entry(main_frm, textvariable=num)
    measure_button = ttk.Button(main_frm, text='Start', command=measure)

    path_label = ttk.Entry(main_frm, textvariable=filename)
    path_button = ttk.Button(main_frm, text="参照", command=get_path)

    sample_label = ttk.Label(main_frm, text='sample name')
    sample_box = ttk.Entry(main_frm, textvariable=sample)

    # ウィジェットの配置
    initialize_button.grid(column=0, row=0)
    jog_label.grid(column=0, row=1)
    jog_box.grid(column=1, row=1)
    jog_button.grid(column=2, row=1)
    rotate_label.grid(column=0, row=2)
    rotate_box.grid(column=1, row=2)
    rotate_button.grid(column=2, row=2)
    volt_label.grid(column=0, row=3)
    #volt_box.grid(column=1, row=3)
    volt_button.grid(column=2, row=3)
    measure_label.grid(column=0, row=4)
    measure_box.grid(column=1, row=4)
    measure_button.grid(column=2, row=4)
    path_label.grid(column=1, row=5)
    path_button.grid(column=2, row=5)
    sample_label.grid(column=0, row=6)
    sample_box.grid(column=1, row=6)

    main_win.columnconfigure(0, weight=1)
    main_win.rowconfigure(0, weight=1)
    main_frm.columnconfigure(1, weight=1)

    main_win.mainloop()


    # for num in range(60):
    #     volt()
    #     time.sleep(2)
    #     move()
    # volt()

