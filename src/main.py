from gcode_manipulation.gcode_parser import GCode_Parser
from gcode_manipulation.gcode_writer import Gcode_Writer
from gcode_manipulation.gcode import GCode
from util.file_handler import File_Handler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = GCode_Parser()
    original_gcode = parser.create_gcode()

    writer = Gcode_Writer(original_gcode)

    modified_gcode: GCode = writer.modify_gcode()

    file_handler = File_Handler()

    file_handler.write_file(modified_gcode.gcode_list)

    # print(len(modified_gcode.time_elapsed_list))
    # print(len(modified_gcode.layer_list))

    # for line in modified_gcode.time_elapsed_list:
    #     print(modified_gcode.gcode_list[line])


    for line in range(len(original_gcode.gcode_list)):
        print("Line: " + str(line))
        print("Original: " + str(original_gcode.gcode_list[line]))
        print("Modified: " + str(modified_gcode.gcode_list[line]))
        print("-------")


