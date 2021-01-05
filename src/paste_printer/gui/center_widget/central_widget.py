from PyQt5.QtWidgets import QGridLayout, QWidget
from paste_printer.gui.left_side.left_side import Left_Side
from paste_printer.gui.menu_bar.menu_bar import Menu_Bar
from paste_printer.util.file_handler import File_Handler


class Central_Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()

        self.grid = QGridLayout()

        self.menu_bar = Menu_Bar()
        self.grid.addWidget(self.menu_bar, 0, 0)

        self.left_side = Left_Side()
        self.grid.addWidget(self.left_side, 1, 0)
        self.left_side.observer = self

        # self.right_side = Right_Side()
        # self.grid.addWidget(self.right_side, 0, 1)

        self.setLayout(self.grid)

        self.left_side.notify_observer()

    def update(self, gcode):
        None
        #self.right_side.load_new_gcode(gcode)
