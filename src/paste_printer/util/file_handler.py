from pathlib import Path
from paste_printer.gcode_manipulation.gcode import GCode

class File_Handler():

    def __init__(self):
        self.root = Path.joinpath(Path(__file__).parents[1], "resources")

        self.gcode_path = Path.joinpath(self.root, "gcode")
        self.font_path = Path.joinpath(self.root, "fonts")
        self.icon_path = Path.joinpath(self.root, "icons")

        self.icon_ico_path = Path.joinpath(self.icon_path, "apple_icon.ico")
        self.icon_png_path = Path.joinpath(self.icon_path, "apple_icon.png")
        self.used_font_path = Path.joinpath(self.font_path, "Eurostile LT Std.otf")

    def read_gcode_file(self, file_path):
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        return line_list

    def write_file(self, gcode: GCode, path, file_name):
        file_name_extension = file_name + ".gcode"
        file_path = Path.joinpath(Path(path), file_name_extension)

        print(gcode.whole_code)

        f = open(file_path, "w")
        f.write(gcode.whole_code)
        f.close()
