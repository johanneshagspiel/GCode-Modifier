import sys

from PyQt5.QtWidgets import QApplication

from gui.mainscreen import Mainscreen

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_screen = Mainscreen()
    sys.exit(app.exec_())