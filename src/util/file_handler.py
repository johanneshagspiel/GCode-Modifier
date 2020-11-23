from pathlib import Path
from gcode_manipulation.gcode import GCode

class File_Handler():

    def __init__(self):
        self.root = Path.joinpath(Path(__file__).parents[1], "main")
        self.resource_path = Path.joinpath(self.root, "resources")

        self.gcode_path = Path.joinpath(self.resource_path, "gcode")
        self.font_path = Path.joinpath(self.resource_path, "fonts")
        self.icon_path = Path.joinpath(self.resource_path, "icons")

        self.original_gcode_path = Path.joinpath(self.gcode_path, "original")
        self.modified_gcode_path = Path.joinpath(self.gcode_path, "modified")

        self.used_icon_path = Path.joinpath(self.icon_path, "apple_icon.ico")
        self.used_font_path = Path.joinpath(self.font_path, "Eurostile LT Std.otf")

    def read_gcode_file(self):
        file_path = Path.joinpath(self.original_gcode_path, "CFFFP_20mm_Calibration_Box (half cube).gcode")
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        return line_list

    def write_file(self, to_write: GCode):
        file_path = Path.joinpath(self.modified_gcode_path, "cube_updated.gcode")

        f = open(file_path, "w")
        f.write("\n".join(to_write.start_gcode))
        f.write("\n\n\n")
        f.write("\n".join(to_write.main_gcode))
        f.write("\n\n\n")
        f.write("\n".join(to_write.end_gcode))
        f.close()