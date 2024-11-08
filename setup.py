import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "sys", "PyQt5", "qrcode", "barcode", "PIL", "json"],
    "include_files": ["Presets.json"],
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
        # Optionally, you can include an icon file for the executable
    )
]

setup(
    name="Measurement Box Generator",
    version="1.0",
    description="An application for generating measurement box codes",
    options={"build_exe": build_exe_options},
    executables=executables
)
