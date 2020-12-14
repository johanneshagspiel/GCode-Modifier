import sys

from PyQt5.QtWidgets import QApplication
from paste_printer.gui.left_side.left_side import Left_Side
from paste_printer.gui.main_screen import Main_Screen

class Application():

    def __init__(self):
        app = QApplication(sys.argv)
        main_screen = Main_Screen()
        main_screen.show()
        sys.exit(app.exec_())
