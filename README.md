<img src=resources/gcode_modifier_logo.JPG alt="G-Code Modifier Logo" width="121" height="128">

--------------------------------------------------------------------------------
[![MIT-License](https://img.shields.io/github/license/johanneshagspiel/gcode-modifier)](LICENSE)
[![Top Language](https://img.shields.io/github/languages/top/johanneshagspiel/gcode-modifier)](https://github.com/johanneshagspiel/gcode-modifier)
[![Latest Release](https://img.shields.io/github/v/release/johanneshagspiel/gcode-modifier)](https://github.com/johanneshagspiel/gcode-modifier/releases/)

# G-Code Modifier

G-Code Modifier is 

## Features

The

## Tools

| Purpose                | Name                                                         |
|------------------------|--------------------------------------------------------------|
| Programming language   | [Python](https://www.python.org/)                            |
| Dependency manager     | [Anaconda](https://www.anaconda.com/products/distribution)   |
| Version control system | [Git](https://git-scm.com/)                                  |
| Testing framework      | [unittest](https://docs.python.org/3/library/unittest.html/) |
| Application Bundler    | [PyInstaller](https://pyinstaller.org/en/stable/index.html/) |


## Installation Process

A precompiled executable can be found with the [latest release]((https://github.com/johanneshagspiel/gcode-modifier/releases/)). 

If you want to build the application yourself, it is assumed that you have installed [Python](https://www.python.org/downloads/windows/) and that your operating system is Windows.

Open this repository in the terminal of your choice. In case `pip` has not been installed, do so via:

    py -m ensurepip --upgrade

Install `pyinstaller` with this command:

    pip install -U pyinstaller

Now, create the executable via:

    cd src | pyinstaller paste_printer/main.py --distpath "pyinstaller/dist" --workpath "pyinstaller/build"  --noconsole --add-data "paste_printer/resources/icons/*;paste_printer/resources/icons" --add-data "paste_printer/resources/gcode/0.6/*;paste_printer/resources/gcode/0.6" --add-data "paste_printer/resources/gcode/0.8/*;paste_printer/resources/gcode/0.8" --add-data "paste_printer/resources/gcode/1.5/*;paste_printer/resources/gcode/1.5" --add-data "paste_printer/resources/fonts/*;paste_printer/resources/fonts" --add-data "paste_printer/resources/settings/*;paste_printer/resources/settings"

This should have created a new folder in `src` called `pyinstaller`. The executable can be then be found at `src/pyinstaller/dist/main.exe`

## Licence

The G-Code Modifier is published under the MIT licence, which can be found in the [LICENSE](LICENSE) file.