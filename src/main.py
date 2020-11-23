from gcode_manipulation.gcode_parser import GCode_Parser
from gcode_manipulation.gcode_writer import Gcode_Writer
from gcode_manipulation.gcode import GCode
from util.file_handler import File_Handler
from gui.main_screen import MainScreen
import sys
import os

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # parser = GCode_Parser()
    # original_gcode = parser.create_gcode()
    #
    # writer = Gcode_Writer(original_gcode)
    #
    # modified_gcode: GCode = writer.modify_gcode()
    #
    # file_handler = File_Handler()
    # file_handler.write_file(modified_gcode)

    main_screen = MainScreen()
    main_screen.start()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
