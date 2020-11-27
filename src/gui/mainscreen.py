import ctypes
import os
import subprocess
from pathlib import Path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5 import QtCore
from PyQt5 import QtGui

from command.command import Command
from command.command_executor import Command_Executor
from gui.customization.load_font import load_font
from util.file_handler import File_Handler

class Mainscreen(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()

        #Create program name
        program_name="Paste Printer G-code Modifier - Version "
        program_version ="0.1"

        #Set Name Of Program
        self.setWindowTitle(program_name + program_version)

        #change program icon
        self.setWindowIcon(QtGui.QIcon(str(self.file_handler.icon_png_path)))

        #change Font
        load_font(self.file_handler.used_font_path)
        self.setFont(QFont("Eurostile LT Std", 18))

        #change taskbar icon
        myappid = program_name + program_version  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #Set size of Window (Starting x, starting y, width, height
        self.setGeometry(180, 180, 720, 720)

        #Create Grid
        self.grid = QGridLayout()

        #row pointer
        row_position = 0

        #Nozzle Size Selection
        nozzle_size_selection_label = QLabel("With with nozzle size do you want to print?")
        nozzle_size_selection_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(nozzle_size_selection_label, row_position, 0, 1, 2)
        row_position += 1

        #Nozzle Selection HBox
        nozzle_size_selection_hobx = QHBoxLayout()
        self.grid.addLayout(nozzle_size_selection_hobx, row_position, 0, 1, 2)
        row_position += 1

        #Nozzle 1.3 Size Button
        self.nozzle_1_3_button = QRadioButton("1.3 mm")
        self.nozzle_1_3_button.setChecked(True)
        self.nozzle_1_3_button.toggled.connect(lambda:self.update_files("1.3"))
        nozzle_size_selection_hobx.addWidget(self.nozzle_1_3_button, QtCore.Qt.AlignLeft)

        #Nozzle 1.3 Size Button
        self.sdf = QRadioButton("sdf")
        self.sdf.toggled.connect(lambda:self.update_files("sdf"))
        nozzle_size_selection_hobx.addWidget(self.sdf, QtCore.Qt.AlignLeft)

        #File Selection Label
        file_selection_label = QLabel("Which file do you want to modify?")
        file_selection_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(file_selection_label, row_position, 0, 1, 2)
        row_position += 1

        #Radiobutton for each gcode
        file_list = []
        file_paths = sorted(self.file_handler.gcode_path.glob('*.gcode'))
        for file in file_paths:
            file_list.append(os.path.splitext(file.name)[0])

        for index, file in enumerate(file_list):
            temp = QRadioButton(file)
            if index == 0:
                temp.setChecked(True)
                self.selected_file_name = file
            temp.toggled.connect(lambda _, file=file: self.update_name_selected_file(file))
            self.grid.addWidget(temp, row_position, 0, 1, 2)
            row_position += 1

        #Print setting label
        print_settings_label = QLabel("Which print settings do you want to use?")
        print_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(print_settings_label, row_position, 0, 1, 2)
        row_position += 1

        #Flow Rate Label
        flow_rate_label = QLabel("Flow rate: ")
        flow_rate_label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(flow_rate_label,row_position, 0)

        # Flow Rate Entry
        self.flow_rate_entry = QLineEdit()
        self.flow_rate_entry.setText("55")
        self.grid.addWidget(self.flow_rate_entry, row_position, 1)
        row_position += 1

        #Bed Temperature Label
        bed_temperature_label = QLabel("Bed Temperature: ")
        bed_temperature_label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(bed_temperature_label,row_position, 0)

        #Bed Temperature Entry
        self.bed_temperature_entry = QLineEdit()
        self.bed_temperature_entry.setText("0")
        self.grid.addWidget(self.bed_temperature_entry, row_position, 1)
        row_position += 1

        #Modification label
        print_modifications_label = QLabel("What do you want to modify?")
        print_modifications_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(print_modifications_label, row_position, 0, 1, 2)
        row_position += 1

        #Modification Grid
        self.modification_grid = QGridLayout()
        self.grid.addLayout(self.modification_grid, row_position, 0, 1, 2)
        row_position += 1

        # Add Information Checkbox
        self.add_information_checkbox = QCheckBox("Show additional information while printing")
        self.modification_grid.addWidget(self.add_information_checkbox, 0, 0)
        row_position += 1

        #Pause after each layer checkbox
        self.pause_print_checkbox = QCheckBox("Pause print after each layer")
        self.pause_print_checkbox.toggled.connect(self.pause_print_toggled)
        self.modification_grid.addWidget(self.pause_print_checkbox, 1, 0)

        #Pauser after each layer seconds label
        self.pause_print_seconds_label = QLabel("Seconds: ")

        # Pauser after each layer seconds entry
        self.pause_print_seconds_entry = QLineEdit("10")

        #Retract syringe at the end of print Checkbox
        self.retract_syringe_checkbox = QCheckBox("Retract the syringe at the end of print")
        self.modification_grid.addWidget(self.retract_syringe_checkbox, 2, 0)
        row_position += 1

        #Modification label
        storage_label = QLabel("How do you want to store the file?")
        storage_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(storage_label, row_position, 0, 1, 2)
        row_position += 1

        # Name of Modified File Label
        storage_name_label = QLabel("Name modified file: ")
        storage_name_label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(storage_name_label, row_position, 0)

        # Name of Modified File Entry
        self.storage_name_entry = QLineEdit()
        self.storage_name_entry.setText(self.selected_file_name)
        self.grid.addWidget(self.storage_name_entry, row_position, 1)
        row_position += 1

        #Storage Path Label
        self.path_label = QLabel("Storage path: ")
        self.grid.addWidget(self.path_label, row_position, 0)

        # Chose Location to store button
        self.choose_location_button = QPushButton("Choose location to store")
        self.last_directory = ""
        self.choose_location_button.clicked.connect(self.select_storage_location)
        self.grid.addWidget(self.choose_location_button, row_position, 1)
        self.row_position_path = row_position
        row_position += 1

        #Storage Path Name Label
        self.path_name_label = QLabel()

        #Set layout and show mainscreen
        self.setLayout(self.grid)
        self.show()

        #Modify Button
        self.modify_button = QPushButton("Modify!")
        self.modify_button.clicked.connect(self.start_modification)
        self.grid.addWidget(self.modify_button, row_position, 0, 1, 2)

    def update_files(self, size):
        sender = self.sender()
        if sender.isChecked():
            print(size)

    def pause_print_toggled(self):
        checkbx = self.sender()
        if checkbx.isChecked():
            self.modification_grid.addWidget(self.pause_print_seconds_label, 1, 1)
            self.modification_grid.addWidget(self.pause_print_seconds_entry, 1, 2)
        else:
            self.pause_print_seconds_label.setParent(None)
            self.pause_print_seconds_entry.setParent(None)

    def update_name_selected_file(self, file):
        sender = self.sender()
        if sender.isChecked():
            self.storage_name_entry.setText(file)
            self.selected_file_name = file

    def select_storage_location(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if len(directory) == 0 & len(self.last_directory) != 0:
            directory = self.self.last_directory

        self.path_name_label.setText(directory)
        self.last_directory = directory

        self.grid.addWidget(self.path_name_label, self.row_position_path, 1)

        #Shift Everything below the new path text one row down
        self.choose_location_button.setText("Choose a different location")
        self.grid.addWidget(self.choose_location_button, self.row_position_path + 1, 0, 1, 2)
        self.grid.addWidget(self.modify_button, self.row_position_path + 2, 0, 1, 2)

    def start_modification(self):
        checked_command = self.sanity_check()

        if checked_command != False:
            command_executor = Command_Executor(checked_command)
            command_executor.execute()

            finish_modification_message = QMessageBox()
            finish_modification_message.setText("File has been created successfully!")
            finish_modification_message.setWindowTitle("File Creation Successful")
            finish_modification_message.setIcon(QMessageBox.Information)

            open_location_button = QPushButton("Open File Location")
            open_location_button.clicked.connect(lambda: self.open_directory(checked_command.storage_path))

            open_notebook_button = QPushButton("Open File in Notebook")
            path_to_file = checked_command.storage_path + "\/" + checked_command.file_name + ".gcode"
            open_notebook_button.clicked.connect(lambda: self.open_notebook(path_to_file))

            finish_modification_message.addButton(open_location_button, QMessageBox.AcceptRole)
            finish_modification_message.addButton(open_notebook_button, QMessageBox.AcceptRole)

            finish_modification_message.setStandardButtons(QMessageBox.Ok)

            finish_modification_message.exec_()

    def sanity_check(self):
        messages = []

        flow_rate = self.flow_rate_entry.text()
        try:
            int_flow_rate = int(flow_rate)
            if int_flow_rate < 10 or int_flow_rate > 400:
                raise Exception
        except Exception:
            messages.append("The flow rate needs to be an integer between 10 and 400.")
            self.flow_rate_entry.setText("")

        bed_temperature = self.bed_temperature_entry.text()
        try:
            int_bed_temperature = int(bed_temperature)
            if int_bed_temperature < 0 or int_bed_temperature > 60:
                raise Exception
        except Exception:
            messages.append("The bed temperature needs to be an integer between 0 and 60.")
            self.bed_temperature_entry.setText("")

        storage_location = self.path_name_label.text()
        if len(storage_location) == 0:
            messages.append("A storage location needs to be specified.")

        file_name = self.storage_name_entry.text()
        if len(file_name) == 0:
            messages.append("A filename needs to be specified.")

        if self.pause_print_checkbox.isChecked():
            try:
                int_duration_pause = int(self.pause_print_seconds_entry.text())
                if int_duration_pause < 0 or int_duration_pause > 1800:
                    raise Exception
            except Exception:
                messages.append("The duration of the pause needs to be an integer between 0 and 1800.")
                self.pause_print_seconds_entry.setText("")

        if len(messages) > 0:
            error_text = "\n".join(messages)
            error_message_box = QMessageBox()
            error_message_box.setText(error_text)
            error_message_box.setWindowTitle("Input Error")
            error_message_box.setIcon(QMessageBox.Warning)
            error_message_box.exec_()
            return False

        else:
            file_name_with_extension = self.selected_file_name + ".gcode"
            path_to_file = Path.joinpath(self.file_handler.gcode_path, file_name_with_extension)
            additional_information_bol = self.add_information_checkbox.isChecked()
            pause_each_layer_bol = self.pause_print_checkbox.isChecked()
            retract_syringe_bol = self.retract_syringe_checkbox.isChecked()

            pause_each_layer_par = None
            if pause_each_layer_bol == True:
                pause_each_layer_par = self.pause_print_seconds_entry.text()

            return Command(path_to_file=path_to_file,
                           flow_rate=int_flow_rate, bed_temperature=int_bed_temperature,
                           additional_information_bol=additional_information_bol,
                           pause_each_layer_bol=pause_each_layer_bol,
                           retract_syringe_bol=retract_syringe_bol,
                           file_name=file_name, storage_path=storage_location,
                           pause_each_layer_par=pause_each_layer_par)

    def open_directory(self, directory):
        os.startfile(directory)

    def open_notebook(self, directory):
        subprocess.Popen(["notepad.exe", directory])
