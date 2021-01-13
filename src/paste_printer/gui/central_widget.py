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
        self.settings = self.file_handler.read_settings()

        self.grid = QGridLayout()

        self.menu_bar = Menu_Bar(self.settings)
        self.grid.addWidget(self.menu_bar, 0, 0)
        self.menu_bar.observer = self

        self.left_side = Left_Side(self.settings)
        self.grid.addWidget(self.left_side, 1, 0)
        self.left_side.observer = self

        self.setLayout(self.grid)

        self.left_side.notify_observer()

    def update(self, type, par1, par2 = None):
        if type == "left_side":
            None
            #self.right_side.load_new_gcode(par1)
        if type == "menu_bar":
            self.left_side.uncheck_all_nozzle_size_buttons()
            if par1 == "1.5":
                self.left_side.nozzle_1_5_button.setChecked(True)
            if par1 == "0.8":
                self.left_side.nozzle_0_8_button.setChecked(True)
            if par1 == "0.6":
                self.left_side.nozzle_0_6_button.setChecked(True)

            self.left_side.update_diameter(par1)
            self.left_side.uncheck_all_file_buttons()
            self.left_side.check_file_button(par2)

        if type == "new_settings":
            new_settings = par1

            self.settings = new_settings
            self.left_side.settings = new_settings
            self.menu_bar.settings = new_settings

            self.file_handler.settings_to_file(self.settings)
