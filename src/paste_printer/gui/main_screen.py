import ctypes

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow

from paste_printer.gui.central_widget import Central_Widget
from paste_printer.gui.customization.load_font import load_font
from paste_printer.util.file_handler import File_Handler


class Main_Screen(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file_handler = File_Handler()

        # Create program name
        program_name = "G-Code Modifier "
        program_version = "1.2"

        # Set Name Of Program
        self.setWindowTitle(program_name + program_version)

        # change program icon
        self.setWindowIcon(QIcon(str(self.file_handler.icon_png_path)))

        # change Font
        load_font(self.file_handler.used_font_path)
        self.setFont(QFont("Eurostile LT Std", 18))
        heading_font = QFont("Eurostile LT Std", 18, weight=QFont.Bold)

        # change taskbar icon
        myappid = program_name + program_version  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Set name of Window (Starting x, starting y, width, height
        #self.setGeometry(180, 180, 720, 720)

        # Add left hand side
        central_widget = Central_Widget()
        self.setCentralWidget(central_widget)
