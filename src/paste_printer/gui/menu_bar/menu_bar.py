from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog
from shutil import copy

from paste_printer.gui.menu_bar.select_nozzle_window import Select_Nozzle_Window
from paste_printer.util.file_handler import File_Handler


class Menu_Bar(QMenuBar):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()
        file_menu = self.addMenu("Files")

        add_file_action = QAction("Add GCode File", self)
        file_menu.addAction(add_file_action)

        add_file_action.triggered.connect(self.add_file_action)

    def add_file_action(self):
        selected_nozzle_size = Select_Nozzle_Window.get_nozzle_size()
        dest = 0

        if selected_nozzle_size =="0.6 mm":
            dest = self.file_handler.diameter_0_6_path
        if selected_nozzle_size =="0.8 mm":
            dest = self.file_handler.diameter_0_8_path
        if selected_nozzle_size =="1.5 mm":
            dest = self.file_handler.diameter_1_5_path

        if selected_nozzle_size != 0:

            dialog = QFileDialog(self).getOpenFileName(caption="Select A GCode File That You Want To Add", filter="GCode (*.gcode)", initialFilter="GCode (*.gcode)")
            src = dialog[0]

            copy(src, dest)
