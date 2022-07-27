import requests
import json
import time
from datetime import datetime as t
from PyQt5 import QtWidgets,QtCore,QtGui
import pyqtgraph as pg
import sys
import traceback
import psutil
import pyqtgraph.exporters
from wallpaper import get_wallpaper, set_wallpaper


url = "https://api.webstorage.jp/v1/devices/current"
api_key = "voeknmiivbe4ffk17d0gl2h3t06257su5ei8c0hauo1v5"
login_id = "tbac1967"
password = "hikaribussei"
paylord = {'api-key': api_key, "login-id": login_id, 'login-pass': password}
header = {'Host': 'api.webstrage.js:443', 'Content-Type': 'application/json', 'X-HTTP-Method-Override': 'GET'}

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("おんどとりAPI")
        self.main_widget = QtWidgets.QWidget()  # Create a primary component
        self.main_layout = QtWidgets.QGridLayout()  # Create a grid layout
        self.main_widget.setLayout(self.main_layout)  # Set the layout of the main component for the grid
        self.setCentralWidget(self.main_widget)  # Set the window default part

        self.plot_widget = QtWidgets.QWidget()  # Instantiate a Widget component as a K-line map component
        self.plot_layout = QtWidgets.QGridLayout()  # Instantiate a grid layout
        self.plot_widget.setLayout(self.plot_layout)  # Set the layout of the K-line map part
        self.plot_plt = pg.PlotWidget()  # Instantiate a drawing component
        self.plot_plt.showGrid(x=True,y=True) # Show graphical grid
        self.plot_layout.addWidget(self.plot_plt)  # Add a grid layout of the drawing part to the K line map
        # Add the above components to the layout
        self.main_layout.addWidget(self.plot_widget, 1, 0, 3, 3)
        
        self.setCentralWidget(self.main_widget)
        self.plot_plt.setYRange(max=23,min=17)
        self.plot_plt.setLabels(bottom="Time", left="Temperature (K)")
        self.data_list = []
        self.timer_start()

    #     Timer time interval
    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.readData)
        self.timer.start(60000)

    def readData(self):
        try:
            response = requests.post(url, json.dumps(paylord).encode('utf-8'), headers=header).json()
            #name = response['devices'][0]['name']
            battery = response['devices'][0]['battery']
            temp = response['devices'][0]['channel'][0]['value']  # +" deg.-C")
            #humid = response['devices'][0]['channel'][1]['value']  # + " %")
            #print(name, battery, temp, humid)
            print(t.now(), temp+" C", battery)
            self.data_list.append(float(temp))
            self.plot_plt.plot().setData(self.data_list, pen='g')
            pg.QtGui.QApplication.processEvents()
            exporter = pg.exporters.ImageExporter(self.plot_plt.scene())
            exporter.export("screen.png")
            #return temp
        except Exception as e:
            print(traceback.print_exc())

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()