from pathlib import Path
from tkinter import Frame, Label, Tk, Button
import ctypes

from gui.customizations.styles import Styles
from gui.customizations.load_font import load_font
from util.file_handler import File_Handler


class MainScreen:

    def __init__(self):
        self.master = Tk()
        self.file_handler = File_Handler()

        program_name="Paste Printer G-code Modifier - Version "
        program_version ="0.1"

        self.master.title(program_name + program_version)
        self.master.geometry("%dx%d+%d+%d" % (720, 720, 160, 56))
        self.master.resizable(width=False, height=False)

        #updates the taskbar icon
        myappid =program_name + program_version # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #updates the application window icon
        print(self.file_handler.used_icon_path)
        self.master.iconbitmap(True, self.file_handler.used_icon_path)

        #loads custom font
        load_font(self.file_handler.used_font_path)

        self.center_frame = Frame(self.master, width=720, height=720, background="white")
        self.center_frame.grid(row=0, column=0, sticky='nsew')
        self.center_frame.grid_propagate(0)

        self.file_selection_label = Label(self.center_frame, text="Which file do you want to modify?", **Styles.label_style)
        self.file_selection_label.grid(row=0, column=0, sticky='w')

        file_paths = sorted(self.file_handler.original_gcode_path.glob('*.gcode'))
        file_button_index = 0
        for file in file_paths:
            self.file_button = Button(self.center_frame, text=str(file.name),
					command=None,
					bg="white")
            self.file_button.grid(row=1, column=file_button_index, sticky ='w')
            file_button_index += 1

            #update is needed otherwise size is not accurately reflected
            self.file_button.update()

    def start(self):
        self.master.lift() #starts on top of all other applications
        self.master.mainloop()
