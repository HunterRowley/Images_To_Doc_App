# https://www.iditect.com/faq/python/how-to-hide-the-console-window-when-freezing-wxpython-applications-with-cxfreeze.html#:~:text=To%20hide%20the%20console%20window%20when%20freezing%20a,application%2C%20the%20console%20window%20will%20not%20be%20displayed.
# https://stackoverflow.com/questions/52104043/cannot-compile-with-cx-freeze

import sys
from cx_Freeze import setup, Executable
import os
sys.setrecursionlimit(5000)

current_directory = os.getcwd()

# In the pycharm terminal:
# cd to the same directory as this program and the program that an executable is being created of,
# In the same terminal, type in the command "python setup.py build" to start the process

options = {
    "build_exe": {
        "includes": ["wx"],
    },
}

executables = [
    Executable(
        # "Generate_Employee_Tag.py",
        "ETG_Tkinter_Window.py",
        base="Win32GUI",
        # icon="C:\pythonProject\Employee_Tag_Generator\hunter_DM.png"
        icon=current_directory + "\\" + "hunter_DM.png"
    )
]

setup(
    name="Create Data Matrix",
    version="1.0",
    author="Hunter Rowley",
    description="From a CSV file of employee names and their ID number, generate PNG files of each data matrix",
    executables=executables
)

# setup(
#     name="Create Data Matrix",
#     version="1.0",
#     author="Hunter Rowley",
#     description="From a CSV file of employee names and their ID number, generate PNG files of each data matrix",
#     executables=[
#         Executable("C:\pythonProject\Employee_dataMatrix_Generator",
#                    icon="C:\pythonProject\Valknut.svg",
#                    shortcut_name="Generate Data Matrix",
#                    shortcut_dir="DesktopFolder")
#     ]
# )