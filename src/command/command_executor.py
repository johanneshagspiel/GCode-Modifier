from command.command import Command
from command.task import Task
from gcode_manipulation.gcode_parser import GCode_Parser
from gcode_manipulation.gcode_writer import Gcode_Writer
from util.file_handler import File_Handler

class Command_Executor:

    def __init__(self, command: Command):
        self.command = command
        self.file_handler = File_Handler()

        self.gcode = None
        self.gcode_parser = None
        self.gcode_writer = Gcode_Writer()

    def execute(self):
        #Read the gcode from file
        line_list = self.file_handler.read_gcode_file(file_path=self.command.path_to_file)

        #Parse and clean the gcode
        self.gcode_parser = GCode_Parser(line_list=line_list)
        self.gcode = self.gcode_parser.create_gcode()

        #Set Flowrate
        self.execute_task(Task.SET_FLOWRATE, self.command.flow_rate)

        #Set bed temperature
        self.execute_task(Task.SET_BED_TEMPERATURE, self.command.bed_temperature)

        #Check if add information was ticked
        if self.command.additional_information_bol == True:
            self.execute_task(Task.ADDITIONAL_INFORMATION)

        #Check if pause after each layer was ticked
        if self.command.pause_each_layer_bol == True:
            self.execute_task(Task.PAUSE_EACH_LAYER, self.command.pause_each_layer_par)

        # Check if retract syringe was ticked
        if self.command.retract_syringe_bol == True:
            self.execute_task(Task.RETRACT_SYRINGE)

        #Write to file
        self.file_handler.write_file(gcode=self.gcode, path=self.command.storage_path, file_name=self.command.file_name)

    def execute_task(self, task, parameter_1 = None):

        self.gcode_writer.set_gcode(self.gcode)

        if task == Task.SET_FLOWRATE:
            result_gcode = self.gcode_writer.set_flowrate(parameter_1)
        if task == Task.SET_BED_TEMPERATURE:
            result_gcode = self.gcode_writer.set_bed_temperature(parameter_1)

        if task == Task.ADDITIONAL_INFORMATION:
            result_gcode = self.gcode_writer.additional_information()
        if task == Task.PAUSE_EACH_LAYER:
            result_gcode = self.gcode_writer.pause_each_layer(parameter_1)
        if task == Task.RETRACT_SYRINGE:
            result_gcode = self.gcode_writer.retract_syringe()

        self.gcode_parser.set_gcode(result_gcode)
        self.gcode = self.gcode_parser.find_indexes()
