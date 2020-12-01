import shutil
from pathlib import Path
import os

class Temp_File_Handler():

    def __init__(self):
        self.root = Path.joinpath(Path(__file__).parents[1], "test_file_handling")

        self.test_gcode = Path.joinpath(self.root, "test.gcode")
        self.temp_files = Path.joinpath(self.root, "temp_files")

    def delete_all_temp_files(self):

        for filename in os.listdir(self.temp_files):
            file_path = os.path.join(self.temp_files, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
