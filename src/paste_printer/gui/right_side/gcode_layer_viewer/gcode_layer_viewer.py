from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout

from paste_printer.gcode_manipulation.gcode.layer import Layer
from paste_printer.gui.right_side.gcode_layer_viewer.gcode_canvas import GCode_Canvas


class GCode_Layer_Viewer(QWidget):

    def __init__(self):
        super().__init__()

        self.gcode = None
        self.layer = None
        self.overall_x = None
        self.overall_y = None
        self.overall_color = None
        self.max_iteration = 0
        self.current_iteration = 2

        self.initUI()

    def set_gcode(self, gcode):
        self.gcode = gcode
        self.load_layer(0, True)

    def load_layer(self, index, animation):
        self.layer = self.gcode.layer_list[index]
        self.overall_x = self.layer.x_data
        self.overall_y = self.layer.y_data
        self.overall_color = self.layer.color_data

        self.max_iteration = len(self.layer.x_data)
        self.current_iteration = 2

        if animation:
            self.start_showing_animation()
        else:
            self.start_showing_static()

    def initUI(self):
        self.grid = QGridLayout()
        self.canvas = GCode_Canvas(self, width=5, height=4, dpi=100)
        self.grid.addWidget(self.canvas, 0, 0)
        self.setLayout(self.grid)

    def start_showing_static(self):
        self.xdata = self.overall_x
        self.ydata = self.overall_y
        self.colordata = self.overall_color

        self.canvas.axes.cla()
        self.canvas.axes.plot(self.xdata, self.ydata, "-r")
        self.canvas.draw()
        self.show()

    def start_showing_animation(self):
        self.xdata = self.overall_x[0]
        self.ydata = self.overall_y[0]
        self.colordata = self.overall_color[0]

        self.canvas.axes.cla()
        self.canvas.axes.plot(self.xdata, self.ydata, "-r")
        self.canvas.draw()
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):

        self.xdata = self.overall_x[:self.current_iteration]
        self.ydata = self.overall_y[:self.current_iteration]
        self.colordata = self.overall_color[:self.current_iteration]

        self.canvas.axes.cla()
        self.canvas.axes.plot(self.xdata, self.ydata, "-r")
        self.canvas.draw()

        self.current_iteration += 1

        if self.current_iteration == self.max_iteration:
            self.current_iteration = 2

        self.canvas.draw()
