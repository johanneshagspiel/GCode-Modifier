import unittest
from pathlib import Path

from paste_printer.command.command import Command
from paste_printer.command.command_executor import Command_Executor
from test_paste_printer.test_file_handling.temp_file_handler import Temp_File_Handler


class TestCommandExecutor(unittest.TestCase):

    def setUp(self):

        self.test_file_handler = Temp_File_Handler()

        path_to_file = self.test_file_handler.test_gcode
        additional_information_bol = True
        pause_each_layer_bol = True
        retract_syringe_bol = True

        self.test_command = Command(path_to_file=path_to_file,
                       flow_rate_layer_0="100",
                       flow_rate_other_layers="55",
                       bed_temperature="0",
                       additional_information_bol=additional_information_bol,
                       pause_each_layer_bol=pause_each_layer_bol,
                       retract_syringe_bol=retract_syringe_bol,
                       file_name="test",
                       storage_path=self.test_file_handler.temp_files,
                       pause_each_layer_par=10)

    def tearDown(self):
        self.test_file_handler.delete_all_temp_files()

    def test_execute_command(self):
        command_executor = Command_Executor(self.test_command)
        command_executor.execute()