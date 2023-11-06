import glob
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

files = glob.glob("*.ui")
files = files + glob.glob("*.qrc")

for file in files:
    py_file = file.split('.')[0]
    command = f"pyside6-uic {file} -o {py_file}.py"

    if file.split('.')[-1].upper() == 'qrc'.upper():
        path = os.path.join(ROOT_DIR, py_file + '_rc.py')
        command = f"pyside6-rcc {file} -o {path}"

    print('[+]: ' + command)
    os.system(command)
