from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QButtonGroup
from PyQt5 import QtCore
from PyQt5 import QtGui
from paste_printer.gui.right_side.gcode_layer_viewer.gcode_layer_viewer import GCode_Layer_Viewer
from paste_printer.gui.right_side.gcode_3d_viewer.gcode_3d_viewer import Gcode_3D_Viewer
from paste_printer.gui.right_side.gcode_layer_viewer.gcode_layer_viewer_static import GCode_Layer_Viewer_Static


class Right_Side(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 1)

        self.gcode = None
        self.row_position = 0
        self.current_layer = 0
        self.max_layer = 0
        self.animation = False

        self.gcode_layer_viewer = GCode_Layer_Viewer()
        self.gcode_layer_viewer.setHidden(True)
        self.grid.addWidget(self.gcode_layer_viewer, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.gcode_layer_viewer_static = GCode_Layer_Viewer_Static()
        self.grid.addWidget(self.gcode_layer_viewer_static, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.current_layer_label = QLabel("Current Layer: " + str(self.current_layer) + "/" + str(self.max_layer))
        self.grid.addWidget(self.current_layer_label, self.row_position, 0, 1 ,2)
        self.row_position += 1

        self.previous_layer_button = QPushButton("Previous layer")
        self.previous_layer_button.clicked.connect(lambda: self.load_layer(-1))
        self.grid.addWidget(self.previous_layer_button, self.row_position, 0)

        self.next_layer_button = QPushButton("Next layer")
        self.next_layer_button.clicked.connect(lambda: self.load_layer(1))
        self.grid.addWidget(self.next_layer_button, self.row_position, 1)
        self.row_position += 1

        self.turn_on_off_button = QPushButton("Turn Animation On")
        self.turn_on_off_button.clicked.connect(lambda: self.turn_on_off_animation(self.turn_on_off_button.text()))
        self.grid.addWidget(self.turn_on_off_button, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.show_3d_button = QPushButton("Show 3D Animation")
        self.show_3d_button.clicked.connect(self.shop_3d_animation)
        self.grid.addWidget(self.show_3d_button, self.row_position, 0, 1, 2)
        self.row_position += 1

        self.setLayout(self.grid)

    def shop_3d_animation(self):
        gcode_3d_viewer = Gcode_3D_Viewer()
        gcode_3d_viewer.show_with_open3D(self.gcode.layer_list)

    def turn_on_off_animation(self, text):
        if text == "Turn Animation On":
            self.turn_on_off_button.setText("Turn Animation Off")
            self.animation = True
            self.gcode_layer_viewer.setHidden(False)
            self.gcode_layer_viewer_static.setHidden(True)
            self.gcode_layer_viewer.set_gcode(self.gcode)
            self.gcode_layer_viewer.load_layer(self.current_layer)

        if text == "Turn Animation Off":
            self.turn_on_off_button.setText("Turn Animation On")
            self.animation = False
            self.gcode_layer_viewer_static.setHidden(False)
            self.gcode_layer_viewer.setHidden(True)
            self.gcode_layer_viewer_static.set_gcode(self.gcode)
            self.gcode_layer_viewer_static.load_layer(self.current_layer)

    def load_new_gcode(self, gcode):
        self.current_layer = 0
        self.gcode = gcode
        self.max_layer = len(gcode.layer_list)
        if self.animation:
            self.gcode_layer_viewer.set_gcode(gcode)
        else:
            self.gcode_layer_viewer_static.set_gcode(gcode)
        self.update_labels()

    def load_layer(self, index):
        if index == 1 and self.current_layer == (self.max_layer-1):
            self.current_layer = 0
        elif index == -1 and self.current_layer == 0:
            self.current_layer = self.max_layer-1
        else:
            self.current_layer += index

        if self.animation:
            self.gcode_layer_viewer.load_layer(self.current_layer)
        else:
            self.gcode_layer_viewer_static.load_layer(self.current_layer)
        self.update_labels()

    def update_labels(self):
        new_label_text = "Current Layer: " + str(self.current_layer + 1) + "/" + str(self.max_layer)
        self.current_layer_label.setText(new_label_text)
