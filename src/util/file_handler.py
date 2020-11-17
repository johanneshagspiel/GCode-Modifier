from pathlib import Path

class File_Handler():

    def __init__(self):
        self.root = Path(__file__).parents[2]

    def read_file(self):
        file_path = Path.joinpath(self.root, "resources", "CFFFP_20mm_Calibration_Box (half cube).gcode")
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        return line_list

    def write_file(self, to_write):
        file_path = Path.joinpath(self.root, "resources", "test.gcode")

        f = open(file_path, "w")
        f.write("\n".join(to_write))
        f.close()