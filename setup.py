import sys
# sys.setrecursionlimit(90000)
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    # "packages": ["tensorflow", "tkinter", "h5py", "PIL"],
    "zip_include_packages": ["encodings", "PySide6"],
    "includes": ["ttkbootstrap.utility"],
    "excludes": ["problematic_module"],
    "packages":["keras", "tensorflow"],
    # "replace_paths":["*",""]
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Gingivitis Predictor",
    version="0.1",
    description="Gingivitis Predictor",
    options={"build_exe": build_exe_options},
    executables=[Executable("guiBased1.py", base=base,target_name = 'Oral Eye', icon = "oral_eye_icon.ico")]
)



