from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import csv
import igorwriter
import numpy as np
import time
# import threading
# from datetime import datetime

import mercury_client

from repeated_timer import RepeatedTimer

class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        self.mercury_root = "C://Users/hikaribussei/Projects/control_program/control_program/KOhwada"
        self.download_root = "C://Users/hikaribussei/Downloads"

        loadUi(f"{self.mercury_root}/mercury_ui_files/main_window.ui", self)

        self.setWindowTitle("mercury")

        # buttom oprations
        self.startbtn.clicked.connect(self.get_data_loop_func)
        self.stopbtn.clicked.connect(self.stop_flag_up)
        self.clearbtn.clicked.connect(self.clear_graph)
        self.downloadbtn.clicked.connect(self.download)

        # checkbox oprations
        self.csvcheck.stateChanged.connect(self.csv_check_action)
        self.itxcheck.stateChanged.connect(self.itx_check_action)

        self.csv = 1
        self.itx = 1

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.mc = mercury_client.MercuryClient()

        self.kinds = ["TEMP", "POW"]  # 取得するデータの名前

        self.datas = {"DATE": [], "TIME": [], "GETTIME": []}  # 取得データ. 日付と時間は常に取得
        self.elapsed_time = np.array([])  # 経過時間

        self.stop_flag = 0

    def update_graph(self):
        """
        グラフを書く
        """
        self.MplWidget.canvas.axes1.clear()
        self.MplWidget.canvas.axes2.clear()

        for k, v in zip(self.datas.keys(), self.datas.values()):
            if k == "TEMP":
                self.MplWidget.canvas.axes1.plot(self.elapsed_time, v, label=k, marker="o")  # temperature
            elif k == "POW":
                self.MplWidget.canvas.axes2.plot(self.elapsed_time, v, label=k, marker="o")  # power
        
        self.MplWidget.canvas.axes2.set_xlabel("Elapsed time (s)")
        self.MplWidget.canvas.axes1.set_ylabel("Temperature (K)")
        self.MplWidget.canvas.axes2.set_ylabel("Power (W)")
        # self.MplWidget.canvas.axes.legend(loc='upper right')
        self.MplWidget.canvas.draw()
    
    def get_data_loop_func(self):
        """
        stratボタンで起動する関数
        get_data_loop関数を別スレッドで実行する
        uiからintervalを受けとり、定期実行。
        """
        # data_loop_thred = threading.Thread(target=self.get_data_loop)
        # data_loop_thred.start()
        self.start = time.time()  # UNIX時間

        order = ";".join(self.kinds)

        interval = float(self.interval.text())
        self.data_loop_thread = RepeatedTimer(interval, self.get_data, args=(order,))
        self.data_loop_thread.start()

    def get_data_loop(self):
        """
        実際にデータを取得して描画をループする関数
        古いバージョン
        time.sleep()で待ちを作る
        """
        self.start = time.time()  # UNIX時間

        order = ";".join(self.kinds)

        interval = self.interval.text()

        while not self.stop_flag:
            _data_dict = self.mc.get_data_from_mercury(order)  # get data from Mersury
            self._make_datas(_data_dict)
            self.update_graph()

            time.sleep(float(interval))
    
    def get_data(self, order):
        """
        実際にデータを取得し描画する関数
        """
        _data_dict = self.mc.get_data_from_mercury(order)  # get data from Mersury
        self._make_datas(_data_dict)
        self.update_graph()
    
    def _make_datas(self, data_dict):
        """
        1ループ分のデータを辞書型で受け取り、今までのものと結合する。
        """
        # for datetime
        gettime = float(data_dict["GETTIME"])
        delta = gettime - self.start
        self.elapsed_time = np.append(self.elapsed_time, delta)

        # for datas
        _kinds = data_dict.keys()
        _values = data_dict.values()

        for _k, _v in zip(_kinds, _values):
            if _k not in self.datas.keys():
                self.datas[_k] = np.array([])
            
            if _k in ["DATE", "TIME", "GETTIME"]:
                self.datas[_k].append(_v)
            else:
                self.datas[_k] = np.append(self.datas[_k], float(_v))
        
    def stop_flag_up(self):
        """
        stopボタンの処理
        """
        self.data_loop_thread.cancel()
    
    def clear_graph(self):
        self.MplWidget.canvas.axes1.clear()
        self.MplWidget.canvas.axes2.clear()
    
    def download(self):
        name = self.name.text()
        data_list = self.fix_data_for_download()

        if self.csv:
            self.download_as_csv(name, data_list)
        
        if self.itx:
            self.download_as_itx(name, data_list)



    def csv_check_action(self, state):
        if state == 2:
            self.csv = 1
        else:
            self.csv = 0        

    def itx_check_action(self, state):
        if state == 2:
            self.itx = 1
        else:
            self.itx = 0     

    def fix_data_for_download(self):       
        data_array = np.array([], dtype="U1")
        for v in self.datas.values():           
            data_array = np.append(data_array, v)

        rsize = len(self.datas.keys())
        csize = int(data_array.shape[0] / rsize)
        data_array = data_array.reshape(rsize, csize)

        return data_array
    
    def download_as_csv(self, name, data):
        path = f"{self.download_root}/{name}.csv"

        data_list = data.T.tolist()

        with open(path, mode="w") as f:
            writer = csv.writer(f)
            writer.writerow(self.datas.keys())
            writer.writerows(data_list)
    
    def download_as_itx(self, name, data):
        path = f"{self.download_root}/{name}.itx"
        wave_names = self.datas.keys()
        with open(path, mode="w") as f:
            for _wn, _d in zip(wave_names, data):
                if _wn not in ["DATE", "TIME"]:  # only for not string data
                    wave = igorwriter.IgorWave(np.array(_d, dtype=float), name=_wn)
                    wave.save_itx(f)
        

if __name__ == "__main__":
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()