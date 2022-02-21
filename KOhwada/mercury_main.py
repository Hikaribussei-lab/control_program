from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import time
import threading

import mercury_controller
     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("mercury_ui_files/mercury_main_window.ui",self)

        self.setWindowTitle("mercury")

        self.startbtn.clicked.connect(self.get_data_loop_func)
        self.stopbtn.clicked.connect(self.stop_flag_up)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.mc = mercury_controller.MercuryTestController()

        self.temp_datas = np.array([])
        self.stop_flag = 0

    def update_graph(self):

        # fs = 500
        # f = random.randint(1, 100)
        # ts = 1/fs
        # length_of_signal = 100
        # t = np.linspace(0,1,length_of_signal)
        
        # cosinus_signal = np.cos(2*np.pi*f*t)
        # sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(self.temp_datas)
        # self.MplWidget.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
    
    def get_data_loop_func(self):
        data_loop_thred = threading.Thread(target=self.get_data_loop)
        data_loop_thred.start()

    def get_data_loop(self):
        while not self.stop_flag:
            _temp = self.mc.get_data_from_mercury()
            self.temp_datas = np.append(self.temp_datas, _temp)
            self.update_graph()

            time.sleep(0.5)
        
    def stop_flag_up(self):
        self.stop_flag = 1
       

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()