from PyQt5 import QtWidgets,QtCore,QtGui
import pyqtgraph as pg
import sys
import traceback
import psutil

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU usage monitoring - Mr. State https://zmister.com")
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
        self.plot_plt.setYRange(max=100,min=0)
        self.data_list = []
        self.timer_start()

    #     Timer time interval
    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_cpu_info)
        self.timer.start(1000)

    # Get CPU usage
    def get_cpu_info(self):
        try:
            cpu = "%0.2f" % psutil.cpu_percent(interval=1)
            self.data_list.append(float(cpu))
            print(float(cpu))
            self.plot_plt.plot().setData(self.data_list,pen='g')
        except Exception as e:
            print(traceback.print_exc())

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()