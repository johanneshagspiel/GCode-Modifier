from gcode_parser.gcode_parser import GCode_Parser


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = GCode_Parser()
    gcode = parser.create_gcode()

    for index in gcode.layer_index:
        print(gcode.original_gcode[index])
