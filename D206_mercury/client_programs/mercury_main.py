from repeated_timer import RepeatedTimer
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore  # pyqt stuff

QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


import time

import mercury_client
from mercury_run_functions import GetDatas, DownLoad

class MercuryMainWindow(QMainWindow, GetDatas, DownLoad):

    def __init__(self):

        QMainWindow.__init__(self)
        GetDatas.__init__(self)
        DownLoad.__init__(self)

        self.mercury_root = "C:\\Users\hikaribussei\Projects\control_program\control_program\D206_mercury"
        self.download_root = "C:\\Users\hikaribussei\Downloads"

        loadUi(f"{self.mercury_root}\mercury_ui_files\main_window.ui", self)

        self.setWindowTitle("mercury")

        # buttom oprations
        self.mercurystartbtn.clicked.connect(self.mercury_start)
        self.startbtn.clicked.connect(self.get_mercury_data)
        self.stopbtn.clicked.connect(self.stop_operations)
        self.clearbtn.clicked.connect(self.clear_graph)
        self.downloadbtn.clicked.connect(self.download)
        self.mercuryquitbtn.clicked.connect(self.mercury_quit)
        self.serverquitbtn.clicked.connect(self.server_quit)

        # checkbox oprations
        self.csvcheck.stateChanged.connect(self.csv_check_action)
        self.itxcheck.stateChanged.connect(self.itx_check_action)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.mc = mercury_client.MercuryClient()

        self.stop_flag = 0
    
    def mercury_start(self):
        return_string = self.mc.client_main(order="start mercury")
        print(return_string)

    def get_mercury_data(self):
        self.start = time.time()  # UNIX時間

        order = ";".join(self.kinds)

        interval = float(self.interval.text())
        self.data_loop_thread = RepeatedTimer(
            interval, self.get_data_plot, args=(order,))
        self.data_loop_thread.start()

    def stop_operations(self):
        """
        stopボタンの処理
        """
        self.data_loop_thread.cancel()
        return_string = self.mc.client_main(order="stop")
        print(return_string)

    def clear_graph(self):
        self.MplWidget.canvas.axes1.clear()
        self.MplWidget.canvas.axes2.clear()
        
    def mercury_quit(self):
        return_string = self.mc.client_main(order="quit mercury")
        print(return_string)
    
    def server_quit(self):
        return_string = self.mc.client_main(order="quit server")
        print(return_string)

if __name__ == "__main__":
    app = QApplication([])
    window = MercuryMainWindow()
    window.show()
    app.exec_()
