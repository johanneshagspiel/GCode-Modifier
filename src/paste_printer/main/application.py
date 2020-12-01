import sys

from PyQt5.QtWidgets import QApplication

from paste_printer.gui.mainscreen import Mainscreen


class Application():

    def __init__(self):
        app = QApplication(sys.argv)
        main_screen = Mainscreen()
        sys.exit(app.exec_())
