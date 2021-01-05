import ctypes
import os
import subprocess
from pathlib import Path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QButtonGroup
from PyQt5 import QtCore
from PyQt5 import QtGui

from paste_printer.command.command import Command
from paste_printer.command.command_executor import Command_Executor
from paste_printer.gcode_manipulation.gcode.gcode_parser import GCode_Parser
from paste_printer.gui.customization.load_font import load_font
from paste_printer.util.file_handler import File_Handler


class Left_Side(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.observer = None

    def initUI(self):
        self.file_handler = File_Handler()

        #Create program name
        program_name="Paste Printer G-Code Modifier - Version "
        program_version ="0.1"

        #Set Name Of Program
        self.setWindowTitle(program_name + program_version)

        #change program icon
        self.setWindowIcon(QtGui.QIcon(str(self.file_handler.icon_png_path)))

        #change Font
        load_font(self.file_handler.used_font_path)
        self.setFont(QFont("Eurostile LT Std", 18))
        heading_font = QFont("Eurostile LT Std", 18,weight=QtGui.QFont.Bold)

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
        nozzle_size_selection_label = QLabel("With which nozzle size do you want to print?")
        nozzle_size_selection_label.setAlignment(QtCore.Qt.AlignCenter)
        nozzle_size_selection_label.setFont(heading_font)
        self.grid.addWidget(nozzle_size_selection_label, row_position, 0, 1, 2)
        row_position += 1

        #Nozzle Selection HBox
        nozzle_size_selection_hobx = QHBoxLayout()
        self.grid.addLayout(nozzle_size_selection_hobx, row_position, 0, 1, 2)
        row_position += 1

        #Nozzle Selection Buttongroup
        nozzle_size_selection_button_group = QButtonGroup(self)

        #Nozzle 1.3 Size Button
        self.nozzle_1_3_button = QRadioButton("1.5 mm")

        #1.5 diameter is the default
        self.nozzle_1_3_button.setChecked(True)
        self.selected_diameter_path = self.file_handler.diameter_1_5_path

        self.nozzle_1_3_button.toggled.connect(lambda:self.update_diameter("1.5"))
        nozzle_size_selection_button_group.addButton(self.nozzle_1_3_button)
        nozzle_size_selection_hobx.addWidget(self.nozzle_1_3_button, QtCore.Qt.AlignLeft)

        #Nozzle 0.8 Size Button
        self.nozzle_0_8_button = QRadioButton("0.8 mm")
        self.nozzle_0_8_button.toggled.connect(lambda:self.update_diameter("0.8"))
        nozzle_size_selection_button_group.addButton(self.nozzle_0_8_button)
        nozzle_size_selection_hobx.addWidget(self.nozzle_0_8_button, QtCore.Qt.AlignLeft)

        #Nozzle 0.6 Size Button
        self.nozzle_0_6_button = QRadioButton("0.6 mm")
        self.nozzle_0_6_button.toggled.connect(lambda:self.update_diameter("0.6"))
        nozzle_size_selection_button_group.addButton(self.nozzle_0_6_button)
        nozzle_size_selection_hobx.addWidget(self.nozzle_0_6_button, QtCore.Qt.AlignLeft)

        #File Selection Label
        file_selection_label = QLabel("Which file do you want to modify?")
        file_selection_label.setAlignment(QtCore.Qt.AlignCenter)
        file_selection_label.setFont(heading_font)
        self.grid.addWidget(file_selection_label, row_position, 0, 1, 2)
        row_position += 1

        # File Selection Buttongroup
        file_selection_button_group = QButtonGroup(self)

        # File Selection HBox
        file_selection_hobx = QHBoxLayout()
        self.grid.addLayout(file_selection_hobx, row_position, 0, 1, 2)
        row_position += 1

        # Cube Button
        self.cube_button = QRadioButton("Cube")

        # Cube is the default
        self.cube_button.setChecked(True)
        self.selected_file_name = "cube.gcode"

        self.cube_button.toggled.connect(lambda: self.update_file_name("Cube"))
        file_selection_button_group.addButton(self.cube_button)
        file_selection_hobx.addWidget(self.cube_button, QtCore.Qt.AlignLeft)

        # Vase Button
        self.vase_button = QRadioButton("Vase")
        self.vase_button.toggled.connect(lambda: self.update_file_name("Vase"))
        file_selection_button_group.addButton(self.vase_button)
        file_selection_hobx.addWidget(self.vase_button, QtCore.Qt.AlignLeft)

        # Apple Button
        self.apple_button = QRadioButton("Apple")
        self.apple_button.toggled.connect(lambda: self.update_file_name("Apple"))
        file_selection_button_group.addButton(self.apple_button)
        file_selection_hobx.addWidget(self.apple_button, QtCore.Qt.AlignLeft)

        #Print setting label
        print_settings_label = QLabel("Which print settings do you want to use?")
        print_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        print_settings_label.setFont(heading_font)
        self.grid.addWidget(print_settings_label, row_position, 0, 1, 2)
        row_position += 1

        #Print settings grid
        self.print_settings_grid = QGridLayout()
        self.grid.addLayout(self.print_settings_grid, row_position, 0, 1, 2)
        row_position += 1

        #Flow Rate Layer 0 Label
        flow_rate_layer_0_label = QLabel("Flow rate for the first layer: ")
        flow_rate_layer_0_label.setAlignment(QtCore.Qt.AlignLeft)
        self.print_settings_grid.addWidget(flow_rate_layer_0_label, 0, 0)

        # Flow Rate Layer 0 Entry
        self.flow_rate_layer_0_entry = QLineEdit()
        self.flow_rate_layer_0_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.flow_rate_layer_0_entry.setText("100")
        self.print_settings_grid.addWidget(self.flow_rate_layer_0_entry, 0, 1)

        #Toggle Differentiate between Infill / Outer Walls
        self.flow_rate_differentiation_button = QPushButton("Different flow rate for outer walls and infill")
        self.flow_rate_differentiation_button.clicked.connect(lambda: self.differentiate_flow_rate(self.flow_rate_differentiation_button.text()))
        self.print_settings_grid.addWidget(self.flow_rate_differentiation_button, 1, 0, 1, 2)

        #Flow Rate Other Layers
        self.flow_rate_par_1_label = QLabel("Flow rate for the other layers: ")
        self.flow_rate_par_1_label.setAlignment(QtCore.Qt.AlignLeft)
        self.print_settings_grid.addWidget(self.flow_rate_par_1_label, 2, 0)

        # Flow Rate Layer 0 Entry
        self.flow_rate_par_1_entry = QLineEdit()
        self.flow_rate_par_1_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.flow_rate_par_1_entry.setText("100")
        self.print_settings_grid.addWidget(self.flow_rate_par_1_entry, 2, 1)

        # Temp Label
        self.flow_rate_par_2_label = QLabel("Flow rate for the infill: ")
        self.flow_rate_par_2_label.setAlignment(QtCore.Qt.AlignLeft)

        self.print_settings_grid.addWidget(self.flow_rate_par_2_label, 3, 0)
        self.flow_rate_par_2_label.setHidden(True)

        # Temp Entry
        self.flow_rate_par_2_entry = QLineEdit()
        self.flow_rate_par_2_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.flow_rate_par_2_entry.setText("65")

        self.print_settings_grid.addWidget(self.flow_rate_par_2_entry, 3, 1)
        self.flow_rate_par_2_entry.setHidden(True)

        #Bed Temperature Label
        bed_temperature_label = QLabel("Bed Temperature: ")
        bed_temperature_label.setAlignment(QtCore.Qt.AlignLeft)
        self.print_settings_grid.addWidget(bed_temperature_label, 0, 2)

        #Bed Temperature Entry
        self.bed_temperature_entry = QLineEdit()
        self.bed_temperature_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.bed_temperature_entry.setText("0")
        self.print_settings_grid.addWidget(self.bed_temperature_entry, 0, 3)

        #Print Speed Label
        print_speed_label = QLabel("Print Speed: ")
        print_speed_label.setAlignment(QtCore.Qt.AlignLeft)
        self.print_settings_grid.addWidget(print_speed_label, 1, 2)

        #Print Speed Entry
        self.print_speed_entry = QLineEdit()
        self.print_speed_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.print_speed_entry.setText("100")
        self.print_settings_grid.addWidget(self.print_speed_entry, 1, 3)

        #Additional Fan Checkbox
        self.fan_checkbox = QCheckBox("Turn on the fan while printing")
        self.print_settings_grid.addWidget(self.fan_checkbox, 2, 2)

        #Modification label
        print_modifications_label = QLabel("What do you want to modify?")
        print_modifications_label.setAlignment(QtCore.Qt.AlignCenter)
        print_modifications_label.setFont(heading_font)
        self.grid.addWidget(print_modifications_label, row_position, 0, 1, 2)
        row_position += 1

        # Add Information Checkbox
        self.add_information_checkbox = QCheckBox("Show additional information while printing")
        self.grid.addWidget(self.add_information_checkbox, row_position, 0)
        row_position += 1

        #Pause after each layer checkbox
        self.pause_print_retraction_checkbox = QCheckBox("Pause print after each layer")
        self.pause_print_retraction_checkbox.toggled.connect(self.pause_print_toggled)
        self.grid.addWidget(self.pause_print_retraction_checkbox, row_position, 0)
        row_position += 1

        #Pause Choices Grid
        self.grid_choices_grid = QGridLayout()
        self.grid_choices_grid.setColumnMinimumWidth(1, 72)
        self.grid_choices_grid.setColumnMinimumWidth(4, 10)
        self.grid_choices_grid.setColumnStretch(4, 1)
        self.grid.addLayout(self.grid_choices_grid, row_position, 0, 1, 2)
        row_position += 1

        #Pauser after each layer seconds label
        self.pause_print_seconds_label = QLabel("Seconds: ")

        # Pauser after each layer seconds entry
        self.pause_print_seconds_entry = QLineEdit("10")
        self.pause_print_seconds_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.pause_print_seconds_entry.setMaximumWidth(64)

        # Retract During Pause Label
        self.retract_during_pause_checkbox = QCheckBox("Retract during pause")

        #Clean the nozzle ever x moves
        self.clean_nozzle_checkbox = QCheckBox("Clean the nozzle during the print")
        self.grid.addWidget(self.clean_nozzle_checkbox, row_position, 0)
        self.clean_nozzle_checkbox.toggled.connect(self.clean_nozzle_toggled)
        row_position += 1

        #Clean Nozzle Grid
        self.clean_nozzle_grid = QGridLayout()
        self.clean_nozzle_grid.setColumnMinimumWidth(1, 72)
        self.clean_nozzle_grid.setColumnMinimumWidth(4, 10)
        self.clean_nozzle_grid.setColumnStretch(4, 1)
        self.grid.addLayout(self.clean_nozzle_grid, row_position, 0, 1, 2)
        row_position += 1

        #Pauser after each layer seconds label
        self.clean_nozzle_label_1 = QLabel("Every")

        # Pauser after each layer seconds entry
        self.clean_nozzle_entry = QLineEdit("50")
        self.clean_nozzle_entry.setAlignment(QtCore.Qt.AlignCenter)
        self.clean_nozzle_entry.setMaximumWidth(64)

        #Pauser after each layer seconds label
        self.clean_nozzle_label_2 = QLabel("moves")

        #Retract syringe at the end of print Checkbox
        self.retract_syringe_checkbox = QCheckBox("Retract the syringe at the end of print")
        self.grid.addWidget(self.retract_syringe_checkbox, row_position, 0)
        row_position += 1

        #Modification label
        storage_label = QLabel("How do you want to store the file?")
        storage_label.setAlignment(QtCore.Qt.AlignCenter)
        storage_label.setFont(heading_font)
        self.grid.addWidget(storage_label, row_position, 0, 1, 2)
        row_position += 1

        #Storage grid
        self.storage_grid = QGridLayout()
        self.grid.addLayout(self.storage_grid, row_position, 0, 1, 2)
        row_position += 1

        # Name of Modified File Label
        storage_name_label = QLabel("Name modified file: ")
        storage_name_label.setAlignment(QtCore.Qt.AlignLeft)
        self.storage_grid.addWidget(storage_name_label, 0, 0)

        # Name of Modified File Entry
        self.storage_name_entry = QLineEdit()
        self.storage_name_entry.setText(self.selected_file_name.split(".")[0])
        self.storage_grid.addWidget(self.storage_name_entry, 0, 1)

        #Storage Path Label
        self.path_label = QLabel("Storage path: ")
        self.storage_grid.addWidget(self.path_label, 1, 0)

        # Chose Location to store button
        self.choose_location_button = QPushButton("Choose location to store")
        self.last_directory = ""
        self.choose_location_button.clicked.connect(self.select_storage_location)
        self.storage_grid.addWidget(self.choose_location_button, 1, 1)

        row_position += 1
        self.storage_location_button_row = row_position

        #Storage Path Name Label
        self.path_name_label = QLabel()

        #Modify Button
        self.modify_button = QPushButton("Modify!")
        self.modify_button.clicked.connect(self.start_modification)
        self.grid.addWidget(self.modify_button, row_position, 0, 1, 2)

        #Set layout and show mainscreen
        self.setLayout(self.grid)

    def differentiate_flow_rate(self, current_text):

        if current_text == "Different flow rate for outer walls and infill":
            self.flow_rate_differentiation_button.setText("Same flow rate for infill and outer walls")
            self.flow_rate_par_1_label.setText("Flow rate for the outer walls: ")
            self.flow_rate_par_1_entry.setText("55")

            self.flow_rate_par_2_label.setHidden(False)
            self.flow_rate_par_2_entry.setHidden(False)
        else:
            self.flow_rate_differentiation_button.setText("Different flow rate for outer walls and infill")
            self.flow_rate_par_1_label.setText("Flow rate for the other layers: ")
            self.flow_rate_par_1_entry.setText("100")

            self.flow_rate_par_2_label.setHidden(True)
            self.flow_rate_par_2_entry.setHidden(True)

    def update_diameter(self, size):
        sender = self.sender()
        if sender.isChecked():
            if size == "1.5":
                self.selected_diameter_path = self.file_handler.diameter_1_5_path
            if size == "0.8":
                self.selected_diameter_path = self.file_handler.diameter_0_8_path
            if size == "0.6":
                self.selected_diameter_path = self.file_handler.diameter_0_6_path

            self.notify_observer()

    def update_file_name(self, size):
        sender = self.sender()
        if sender.isChecked():
            if size == "Cube":
                self.selected_file_name = "cube.gcode"
                self.storage_name_entry.setText("cube")
            if size == "Vase":
                self.selected_file_name = "vase.gcode"
                self.storage_name_entry.setText("vase")
            if size == "Apple":
                self.selected_file_name = "apple.gcode"
                self.storage_name_entry.setText("apple")

            self.notify_observer()

    def pause_print_toggled(self):
        checkbx = self.sender()
        if checkbx.isChecked():
            self.grid_choices_grid.addWidget(self.pause_print_seconds_label, 1, 2)
            self.grid_choices_grid.addWidget(self.pause_print_seconds_entry, 1, 3)
            self.grid_choices_grid.addWidget(self.retract_during_pause_checkbox, 2, 2)

        else:
            self.pause_print_seconds_label.setParent(None)
            self.pause_print_seconds_entry.setParent(None)
            self.retract_during_pause_checkbox.setParent(None)

    def clean_nozzle_toggled(self):
        checkbx = self.sender()
        if checkbx.isChecked():
            self.clean_nozzle_grid.addWidget(self.clean_nozzle_label_1, 1, 2)
            self.clean_nozzle_grid.addWidget(self.clean_nozzle_entry, 1, 3)
            self.clean_nozzle_grid.addWidget(self.clean_nozzle_label_2, 1, 4)

        else:
            self.clean_nozzle_label_1.setParent(None)
            self.clean_nozzle_entry.setParent(None)
            self.clean_nozzle_label_2.setParent(None)

    def select_storage_location(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if len(directory) == 0 & len(self.last_directory) != 0:
            directory = self.self.last_directory

        self.path_name_label.setText(directory)
        self.last_directory = directory

        self.storage_grid.addWidget(self.path_name_label, 1, 1)

        #Shift Everything below the new path text one row down
        self.choose_location_button.setText("Choose a different location")
        self.grid.addWidget(self.choose_location_button, self.storage_location_button_row, 0, 1, 2)
        self.grid.addWidget(self.modify_button, self.storage_location_button_row + 1, 0, 1, 2)

    def start_modification(self):
        checked_command = self.sanity_check()

        if checked_command != False:
            command_executor = Command_Executor(checked_command)
            result_gcode = command_executor.execute()

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

        flow_rate_layer_0 = self.flow_rate_layer_0_entry.text()
        try:
            int_flow_rate_layer_0 = int(flow_rate_layer_0)
            if int_flow_rate_layer_0 < 10 or int_flow_rate_layer_0 > 400:
                raise Exception
        except Exception:
            messages.append("The flow rate of layer 0 needs to be an integer between 10 and 400.")
            self.flow_rate_layer_0.setText("")

        flow_rate_par_1 = self.flow_rate_par_1_entry.text()
        try:
            int_flow_rate_par_1 = int(flow_rate_par_1)
            if int_flow_rate_par_1 < 10 or int_flow_rate_par_1 > 400:
                raise Exception
        except Exception:
            if self.flow_rate_differentiation_button.text() == "Different flow rate for outer walls and infill":
                messages.append("The flow rate of the other layers needs to be an integer between 10 and 400.")
                self.flow_rate_par_1_entry.setText("100")
            else:
                messages.append("The flow rate for the outer walls needs to be an integer between 10 and 400.")
                self.flow_rate_par_1_entry.setText("55")

        bed_temperature = self.bed_temperature_entry.text()
        try:
            int_bed_temperature = int(bed_temperature)
            if int_bed_temperature < 0 or int_bed_temperature > 60:
                raise Exception
        except Exception:
            messages.append("The bed temperature needs to be an integer between 0 and 60.")
            self.bed_temperature_entry.setText("")

        print_speed = self.print_speed_entry.text()
        try:
            float_print_speed = float(print_speed)
            if float_print_speed < 0 or float_print_speed > 400:
                raise Exception
        except Exception:
            messages.append("The print speed needs to be an integer between 0 and 100.")
            self.print_speed_entry.setText("")

        storage_location = self.path_name_label.text()
        if len(storage_location) == 0:
            messages.append("A storage location needs to be specified.")

        file_name_checked = self.storage_name_entry.text()
        if len(file_name_checked) == 0:
            messages.append("A filename needs to be specified.")

        flow_rate_differentiate_bol = self.flow_rate_differentiation_button.text() == "Same flow rate for infill and outer walls"
        if flow_rate_differentiate_bol:
            flow_rate_par_2 = self.flow_rate_par_2_entry.text()
            try:
                int_flow_rate_par_2 = int(flow_rate_par_2)
                if int_flow_rate_par_2 < 10 or int_flow_rate_par_2 > 400:
                    raise Exception
            except Exception:
                messages.append("The flow rate for the infill needs to be an integer between 10 and 400.")
                self.flow_rate_par_2_entry.setText("65")

        if self.pause_print_retraction_checkbox.isChecked():
            try:
                int_duration_pause = int(self.pause_print_seconds_entry.text())
                if int_duration_pause < 0 or int_duration_pause > 1800:
                    raise Exception
            except Exception:
                messages.append("The duration of the pause needs to be an integer between 0 and 1800.")
                self.pause_print_seconds_entry.setText("")

        if self.clean_nozzle_checkbox.isChecked():
            try:
                int_amount_moves = int(self.clean_nozzle_entry.text())
                if int_amount_moves < 10 or int_amount_moves > 1000:
                    raise Exception
            except Exception:
                messages.append("The amount of moves between cleaning needs to be an integer between 10 and 1000.")
                self.clean_nozzle_entry.setText("")

        if len(messages) > 0:
            error_text = "\n".join(messages)
            error_message_box = QMessageBox()
            error_message_box.setText(error_text)
            error_message_box.setWindowTitle("Input Error")
            error_message_box.setIcon(QMessageBox.Warning)
            error_message_box.exec_()
            return False

        else:
            file_name_checked = file_name_checked.split(".")[0]
            path_to_file = Path.joinpath(self.selected_diameter_path, self.selected_file_name)

            flow_rate_layer_0=int_flow_rate_layer_0
            flow_rate_par_1=int_flow_rate_par_1
            flow_rate_differentiate_bol=flow_rate_differentiate_bol

            fan_bol = self.fan_checkbox.isChecked()

            additional_information_bol = self.add_information_checkbox.isChecked()
            pause_each_layer_bol = self.pause_print_retraction_checkbox.isChecked()
            clean_nozzle_bol = self.clean_nozzle_checkbox.isChecked()
            retract_syringe_bol = self.retract_syringe_checkbox.isChecked()

            flow_rate_par_2 = None
            pause_each_layer_par_1 = None
            pause_each_layer_par_2 = None
            clean_nozzle_par_1 = None

            if flow_rate_differentiate_bol:
                flow_rate_par_2 = int_flow_rate_par_2

            if pause_each_layer_bol:
                pause_each_layer_par_1 = self.pause_print_seconds_entry.text()
                pause_each_layer_par_2 = self.retract_during_pause_checkbox.isChecked()

            if clean_nozzle_bol:
                clean_nozzle_par_1 = self.clean_nozzle_entry.text()

            return Command(path_to_file=path_to_file,

                           flow_rate_layer_0=flow_rate_layer_0,
                           flow_rate_par_1=flow_rate_par_1,
                           flow_rate_differentiate_bol=flow_rate_differentiate_bol,

                           bed_temperature=int_bed_temperature,
                           print_speed=float_print_speed,
                           fan_bol=fan_bol,

                           additional_information_bol=additional_information_bol,
                           pause_each_layer_bol=pause_each_layer_bol,
                           clean_nozzle_bol=clean_nozzle_bol,
                           retract_syringe_bol=retract_syringe_bol,

                           file_name=file_name_checked,
                           storage_path=storage_location,

                           flow_rate_par_2=flow_rate_par_2,

                           pause_each_layer_par_1=pause_each_layer_par_1,
                           pause_each_layer_par_2=pause_each_layer_par_2,

                           clean_nozzle_par_1=clean_nozzle_par_1)

    def open_directory(self, directory):
        os.startfile(directory)

    def open_notebook(self, directory):
        subprocess.Popen(["notepad.exe", directory])

    def notify_observer(self):
        self.path_to_file = Path.joinpath(self.selected_diameter_path, self.selected_file_name)
        new_gocde_line_list = self.file_handler.read_gcode_file(self.path_to_file)
        temp_gcode_parser = GCode_Parser(new_gocde_line_list)
        new_gcode = temp_gcode_parser.create_gcode()
        self.observer.update(new_gcode)
