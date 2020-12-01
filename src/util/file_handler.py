from pathlib import Path
from gcode_manipulation.gcode import GCode

class File_Handler():

    def __init__(self):
        self.root = Path.joinpath(Path(__file__).parents[1], "main")
        self.resource_path = Path.joinpath(self.root, "resources")

        self.gcode_path = Path.joinpath(self.resource_path, "gcode")
        self.font_path = Path.joinpath(self.resource_path, "fonts")
        self.icon_path = Path.joinpath(self.resource_path, "icons")

        self.icon_ico_path = Path.joinpath(self.icon_path, "apple_icon.ico")
        self.icon_png_path = Path.joinpath(self.icon_path, "apple_icon.png")
        self.used_font_path = Path.joinpath(self.font_path, "Eurostile LT Std.otf")

        self.test = Path.joinpath(self.gcode_path, "CFFFP_20mm_Calibration_Box (half cube).gcode")

    def read_gcode_file(self, file_path):
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        return line_list

    def write_file(self, gcode: GCode, path, file_name):
        file_name_extension = file_name + ".gcode"
        file_path = Path.joinpath(Path(path), file_name_extension)

        f = open(file_path, "w")
        f.write(gcode.whole_code)
        f.close()
