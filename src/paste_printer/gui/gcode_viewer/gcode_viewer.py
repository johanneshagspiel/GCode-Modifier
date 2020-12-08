from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from paste_printer.gcode_manipulation.gcode.layer import Layer
from paste_printer.gui.gcode_viewer.gcode_canvas import GCode_Canvas

import matplotlib.pyplot as plt


class GCode_Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

    def show_new_layer(self, layer: Layer):
        self.overall_x = layer.x_data
        self.overall_y = layer.y_data
        self.overall_color = layer.color_data
        self.max_iteration = len(layer.x_data)
        self.current_iteration = 2

        self.start_showing()

    def start_showing(self):

        self.xdata = self.overall_x[0]
        self.ydata = self.overall_y[0]
        self.colordata = self.overall_color[0]

        self.canvas.axes.cla()
        self.canvas.axes.plot(self.xdata, self.ydata, self.colordata)
        self.canvas.draw()
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):

        self.xdata = self.overall_x[:self.current_iteration]
        self.ydata = self.overall_y[:self.current_iteration]
        self.colordata = self.overall_color[:self.current_iteration]

        # self.canvas.axes.cla()
        #
        # for x, y, color in zip(self.xdata, self.ydata, self.colordata):
        #     print(color)
        #     self.canvas.axes.plot(x, y, color)
        #
        # for index, line in enumerate(self.canvas.axes.lines[:]):
        #     print(index)
        #     line.set_color(self.overall_color[index])

        self.canvas.test(self.xdata, self.ydata, self.colordata)
        #
        self.current_iteration += 1

        if self.current_iteration == self.max_iteration:
            self.current_iteration = 2

        self.canvas.draw()


