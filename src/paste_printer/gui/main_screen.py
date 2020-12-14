import ctypes

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QButtonGroup, QMainWindow
from PyQt5 import QtCore
from PyQt5 import QtGui

from paste_printer.gui.center_widget.central_widget import Central_Widget
from paste_printer.gui.customization.load_font import load_font
from paste_printer.gui.left_side.left_side import Left_Side
from paste_printer.util.file_handler import File_Handler


class Main_Screen(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()

        # Create program name
        program_name = "Paste Printer G-Code Modifier - Version "
        program_version = "0.1"

        # Set Name Of Program
        self.setWindowTitle(program_name + program_version)

        # change program icon
        self.setWindowIcon(QtGui.QIcon(str(self.file_handler.icon_png_path)))

        # change Font
        load_font(self.file_handler.used_font_path)
        self.setFont(QFont("Eurostile LT Std", 18))
        heading_font = QFont("Eurostile LT Std", 18, weight=QtGui.QFont.Bold)

        # change taskbar icon
        myappid = program_name + program_version  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Set size of Window (Starting x, starting y, width, height
        #self.setGeometry(180, 180, 720, 720)

        # Add left hand side
        central_widget = Central_Widget()
        self.setCentralWidget(central_widget)
