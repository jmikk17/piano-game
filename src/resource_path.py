import os
import sys


def resource_path(relative_path):
    try:
        # Checking if we are running from pyinstaller
        base_path = sys._MEIPASS
    except Exception:
        # Else get path of dir which this file is in
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
