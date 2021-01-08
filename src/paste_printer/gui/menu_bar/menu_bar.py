from pathlib import Path

from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog
from shutil import copy

from paste_printer.gui.menu_bar.change_environment_window import Change_Environment_Window
from paste_printer.gui.menu_bar.select_nozzle_window import Select_Nozzle_Window
from paste_printer.util.file_handler import File_Handler

class Menu_Bar(QMenuBar):

    def __init__(self, settings):
        super().__init__()

        self.initUI()
        self.observer = None

        self.settings = settings

    def initUI(self):
        self.file_handler = File_Handler()
        file_menu = self.addMenu("Files")

        add_file_action = QAction("Add GCode File", self)
        file_menu.addAction(add_file_action)

        add_file_action.triggered.connect(self.add_file_action)

        settings_menu = self.addMenu("Settings")

        change_settings_action = QAction("Change the Settings", self)
        settings_menu.addAction(change_settings_action)

        change_settings_action.triggered.connect(self.change_settings_action)

    def change_settings_action(self):

        changed_settings = Change_Environment_Window().change_environment(settings=self.settings)
        self.notify_observer("new_settings", changed_settings)

    def add_file_action(self):
        selected_nozzle_size = Select_Nozzle_Window.get_nozzle_size()
        dest = 0

        if selected_nozzle_size =="0.6":
            dest = self.file_handler.diameter_0_6_path
        if selected_nozzle_size =="0.8":
            dest = self.file_handler.diameter_0_8_path
        if selected_nozzle_size =="1.5":
            dest = self.file_handler.diameter_1_5_path

        if selected_nozzle_size != 0:

            dialog,_ = QFileDialog(self).getOpenFileName(caption="Select A GCode File That You Want To Add", filter="GCode (*.gcode)", initialFilter="GCode (*.gcode)")

            if dialog:
                src = dialog

                file_name = Path(src).stem

                copy(src, dest)
                self.notify_observer("menu_bar", selected_nozzle_size, file_name)

    def notify_observer(self, type, par1, par2 = None):

        self.observer.update(type, par1, par2)
