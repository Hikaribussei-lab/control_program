from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from matplotlib import markers

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import time
import threading
from datetime import datetime

import mercury_client


     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        self.mercury_root = "C://Users/hikaribussei/Projects/control_program/control_program/KOhwada"

        loadUi(f"{self.mercury_root}/mercury_ui_files/main_window.ui", self)

        self.setWindowTitle("mercury")

        self.startbtn.clicked.connect(self.get_data_loop_func)
        self.stopbtn.clicked.connect(self.stop_flag_up)
        self.clearbtn.clicked.connect(self.clear_graph)

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
        self.MplWidget.canvas.axes.clear()

        for k, v in zip(self.datas.keys(), self.datas.values()):
            if k not in ["DATE", "TIME", "GETTIME"]:
                self.MplWidget.canvas.axes.plot(self.elapsed_time, v, label=k, marker="o")

        self.MplWidget.canvas.axes.legend(loc='upper right')
        self.MplWidget.canvas.draw()
    
    def get_data_loop_func(self):
        """
        stratボタンで起動する関数
        get_data_loop関数を別スレッドで実行する
        """
        data_loop_thred = threading.Thread(target=self.get_data_loop)
        data_loop_thred.start()

    def get_data_loop(self):
        """
        実際にデータを取得して描画をループする関数
        """
        self.start = time.time()  # UNIX時間

        order = ";".join(self.kinds)

        time_width = self.timewidth.text()

        while not self.stop_flag:
            _data_dict = self.mc.get_data_from_mercury(order)  # get data from Mersury
            self._make_datas(_data_dict)
            self.update_graph()

            time.sleep(float(time_width))
    
    def _make_datas(self, data_dict):
        """
        1ループ分のデータを辞書型で受け取り、今までのものと結合する。
        """
        # for datetime
        gettime = float(data_dict["GETTIME"])
        delta = gettime - self.start
        self.elapsed_time = np.append(self.elapsed_time, delta)
        # print(delta.total_seconds())

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
        self.stop_flag = 1
    
    def clear_graph(self):
        self.MplWidget.canvas.axes.clear()
       

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()