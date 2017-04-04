# -*- coding: utf-8 -*-
"""
    @brief cx_Freeze用のsetup.py
"""

# ----------------------------------------------------------------- import(s)
import sys
from cx_Freeze import setup, Executable

BASE = None
if sys.platform == "win32":
    BASE = None

BUILD_EXE_OPTIONS = {
    "packages": ["cv2", "numpy", "os", "codecs", "configparser", "encodings", "subprocess"],
    "excludes": ["tkinter"],
    "include_files": []
}


setup(
    name="watershed_layer",
    version="1.0",
    description="watershed (PyQt5)",
    author="@MizunagiKB",
    url="",
    options={
        "build_exe": BUILD_EXE_OPTIONS
    },
    executables=[Executable("watershed_layer.py", base=BASE)]
)
