from command.command import Command
from gcode_manipulation.gcode_parser import GCode_Parser
from gcode_manipulation.gcode_writer import Gcode_Writer
from util.file_handler import File_Handler

class Command_Executor:

    def __init__(self, command: Command):
        self.command = command
        self.file_handler = File_Handler()

        self.gcode = None
        self.gcode_parser = None

    def execute(self):
        line_list = self.file_handler.read_gcode_file(file_path=self.command.path_to_file)

        self.gcode_parser = GCode_Parser(line_list=line_list)
        self.gcode = self.gcode_parser.create_gcode()

        gcode_writer = Gcode_Writer()
        print(self.command.retract_syringe_end_of_print)
        if self.command.add_information == 1:
            gcode_writer.set_gcode(self.gcode)
            result_gcode = gcode_writer.add_information_text()
            self.update_gcode(result_gcode)

        if self.command.stop_each_layer == 1:
            gcode_writer.set_gcode(self.gcode)
            result_gcode = gcode_writer.stop_each_layer()
            self.update_gcode(result_gcode)

        if self.command.retract_syringe_end_of_print == 1:
            gcode_writer.set_gcode(self.gcode)
            result_gcode = gcode_writer.retract_syringe_end_of_print()
            self.update_gcode(result_gcode)

        self.file_handler.write_file(gcode=self.gcode, path=self.command.storage_path, file_name=self.command.file_name)

    def update_gcode(self, gcode):
        self.gcode_parser.set_gcode(gcode)
        self.gcode = self.gcode_parser.find_indexes()
