import sys

from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "sys", "PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui", "qrcode", "barcode", "PIL", "json"],
    "include_files": ["Presets.json", "icon.png"],
    "excludes": [],
    "include_msvcr": True,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        icon="favicon.ico"
        # icon="icon.png",
        # Optionally, you can include an icon file for the executable
    )
]

setup(
    name="Measurement Box Generator",
    version="1.0.0.3",
    description="计量箱建档生成器",
    options={"build_exe": build_exe_options},
    executables=executables
)
