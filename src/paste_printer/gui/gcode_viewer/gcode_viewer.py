import numpy as np

from PyQt5 import QtWidgets
import random

from paste_printer.gcode_manipulation.gcode.layer import Layer
from paste_printer.gui.gcode_viewer.gcode_canvas import GCode_Canvas


class GCode_Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

    def show_new_layer(self, layer: Layer):
        n_data = 50

        array = np.array([[1,2,3], [3,4,5]])

        self.xdata = layer.x_data
        self.ydata = layer.y_data
        #self.update_plot()
        # self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

# app = QtWidgets.QApplication(sys.argv)
# w = GCode_Viewer()
# app.exec_()