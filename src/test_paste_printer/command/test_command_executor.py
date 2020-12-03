import unittest
from pathlib import Path

from paste_printer.command.command import Command
from paste_printer.command.command_executor import Command_Executor
from test_paste_printer.util.temp_file_handler import Temp_File_Handler


class TestCommandExecutor(unittest.TestCase):

    def setUp(self):
        self.test_file_handler = Temp_File_Handler()
        self.path_to_file = self.test_file_handler.test_gcode

    def tearDown(self):
        self.test_file_handler.delete_all_temp_files()

    def execute_command(self, command: Command):
        command_executor = Command_Executor(command)
        command_executor.execute()

    def test_command_1(self):
        additional_information_bol = True
        pause_each_layer_bol = True
        retract_syringe_bol = True
        pause_each_layer_par_2 = True

        self.test_command_1 = Command(path_to_file=self.path_to_file,
                                      flow_rate_layer_0="100",
                                      flow_rate_other_layers="55",
                                      bed_temperature="0",
                                      print_speed="100",
                                      fan_bol=True,
                                      additional_information_bol=additional_information_bol,
                                      pause_each_layer_bol=pause_each_layer_bol,
                                      retract_syringe_bol=retract_syringe_bol,
                                      file_name="test",
                                      storage_path=self.test_file_handler.temp_files,
                                      pause_each_layer_par_1=10,
                                      pause_each_layer_par_2=pause_each_layer_par_2)

        self.execute_command(self.test_command_1)

    def test_command_2(self):
        additional_information_bol = True
        pause_each_layer_bol = False
        retract_syringe_bol = True
        pause_each_layer_par_2 = True

        self.test_command_1 = Command(path_to_file=self.path_to_file,
                                      flow_rate_layer_0="100",
                                      flow_rate_other_layers="55",
                                      bed_temperature="0",
                                      print_speed="120",
                                      fan_bol=False,
                                      additional_information_bol=additional_information_bol,
                                      pause_each_layer_bol=pause_each_layer_bol,
                                      retract_syringe_bol=retract_syringe_bol,
                                      file_name="test",
                                      storage_path=self.test_file_handler.temp_files)

        self.execute_command(self.test_command_1)