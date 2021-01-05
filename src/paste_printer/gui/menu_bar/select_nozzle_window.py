from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PyQt5 import QtGui

from paste_printer.util.file_handler import File_Handler


class Select_Nozzle_Window(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.diameter_chosen = 0

        file_handler = File_Handler()

        self.setWindowTitle("Nozzle Size Selection")
        self.setWindowIcon(QtGui.QIcon(str(file_handler.icon_png_path)))

        grid = QGridLayout()

        top_label = QLabel("For which nozzle name do you want to add a GCode file?")
        grid.addWidget(top_label, 0, 0, 1, 3)

        nozzle_0_6_diameter_button = QPushButton("0.6 mm")
        grid.addWidget(nozzle_0_6_diameter_button, 1, 0)
        nozzle_0_6_diameter_button.clicked.connect(lambda: self.set_diameter_chosen(nozzle_0_6_diameter_button.text()))

        nozzle_0_8_diameter_button = QPushButton("0.8 mm")
        grid.addWidget(nozzle_0_8_diameter_button, 1, 1)
        nozzle_0_8_diameter_button.clicked.connect(lambda: self.set_diameter_chosen(nozzle_0_8_diameter_button.text()))

        nozzle_1_5_diameter_button = QPushButton("1.5 mm")
        grid.addWidget(nozzle_1_5_diameter_button, 1, 2)
        nozzle_1_5_diameter_button.clicked.connect(lambda: self.set_diameter_chosen(nozzle_1_5_diameter_button.text()))

        self.setLayout(grid)

    def set_diameter_chosen(self, diameter):
        self.diameter_chosen = diameter
        self.close()

    @staticmethod
    def get_nozzle_size():
        select_nozzle_window = Select_Nozzle_Window()
        select_nozzle_window.exec_()
        return select_nozzle_window.diameter_chosen
