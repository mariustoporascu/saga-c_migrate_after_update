import os

import win32api


def get_version_info(filename):
    """
    Returns the version information of an executable file.
    """
    info = win32api.GetFileVersionInfo(filename, "\\")
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    return f"{win32api.HIWORD(ms)}{win32api.HIWORD(ls)}"

def read_version_info():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(script_dir):
        if file.lower().__eq__('sc.exe'):
            exe_path = os.path.join(script_dir, file)
            try:
                version = get_version_info(exe_path)
                print(f"File: {file}, Version: {version}")
                return version
            except Exception as e:
                print(f"Error reading version for {file}: {e}")
# test
#read_version_info()