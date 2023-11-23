import os.path
import shutil

import PyInstaller.__main__
"""
pyinstaller --noconfirm --onedir --windowed --icon "D:/Code/emedia/logo.ico" --name "EMedia"  "D:/Code/emedia/emedia.py"
"""
PyInstaller.__main__.run([
    'emedia.py',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--icon=logo.ico',
    '--name=EMedia',
])

shutil.copytree('images', os.path.join('dist', 'EMedia', 'images'))
shutil.copytree('icons', os.path.join('dist', 'EMedia', 'icons'))
shutil.copy('Dark.qss', os.path.join('dist', 'EMedia', 'Dark.qss'))
