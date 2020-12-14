from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QButtonGroup, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui

from paste_printer.gui.customization.load_font import load_font
from paste_printer.gui.left_side.left_side import Left_Side
from paste_printer.gui.right_side.right_side import Right_Side
from paste_printer.util.file_handler import File_Handler


class Central_Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()

        self.grid = QGridLayout()

        self.left_side = Left_Side()
        self.grid.addWidget(self.left_side, 0 ,0)
        self.left_side.observer = self

        self.right_side = Right_Side()
        self.grid.addWidget(self.right_side, 0, 1)

        self.setLayout(self.grid)

        self.left_side.notify_observer()

    def update(self, gcode):
        self.right_side.load_new_gcode(gcode)
